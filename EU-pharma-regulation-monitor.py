import argparse
import html
import json
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# EUR-Lex offers RSS feeds for saved searches (account required).
# The feed URL is set via the EURLEX_RSS_URL environment variable.
RSS_URL = os.environ.get("EURLEX_RSS_URL")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")
MODEL = "llama3"

PHARMA_KEYWORDS = ["medicinal", "pharma", "clinical", "health", "medical device", "medicine", "biologic"]
CATEGORIES = [
    "Clinical Trials Transparency",
    "Intellectual Property & Patents",
    "Medical Device Compliance",
    "Not relevant",
]
RELEVANCE = ["high", "medium", "low"]

SYSTEM_PROMPT = f"""
You are an analyst for EU health regulation. Assess the user's EU document for a pharmaceutical company.

Respond only in the following JSON format:
{{
  "category": one of {json.dumps(CATEGORIES, ensure_ascii=False)},
  "relevance": one of {json.dumps(RELEVANCE)},
  "summary": "2-3 sentences",
  "actions": ["concrete public affairs action", "..."]
}}
""".strip()

# Sample documents, used when no RSS feed is configured or reachable
SAMPLE_DOCUMENTS = [
    {
        "title": "Proposal for a Regulation on the European Health Data Space (EHDS)",
        "link": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52022PC0197",
        "date": "2022-05-03",
    },
    {
        "title": "Commission Implementing Decision on harmonised standards for medical devices",
        "link": "https://eur-lex.europa.eu/",
        "date": "Sample",
    },
]


# DATA SOURCE: EUR-LEX RSS FEED

def fetch_eu_pharma_documents(max_docs=5):
    """Reads the EUR-Lex RSS feed and returns health-related documents."""
    if not RSS_URL:
        print("ℹ️  No EURLEX_RSS_URL set, using sample documents.")
        return SAMPLE_DOCUMENTS, True

    print(f"🔎 Loading EUR-Lex feed: {RSS_URL}")
    try:
        response = requests.get(RSS_URL, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"⚠️  Feed unreachable ({e}), using sample documents.")
        return SAMPLE_DOCUMENTS, True

    soup = BeautifulSoup(response.content, "xml")
    documents = []
    for item in soup.find_all("item"):
        title = item.title.text.strip() if item.title else ""
        if any(kw in title.lower() for kw in PHARMA_KEYWORDS):
            documents.append({
                "title": title,
                "link": item.link.text.strip() if item.link else "",
                "date": item.pubDate.text.strip() if item.pubDate else "",
            })

    print(f"   {len(documents)} relevant documents found.")
    return documents[:max_docs], False


# ANALYSIS: LOCAL LLM VIA OLLAMA

def analyze_with_ollama(document):
    """Has a local Llama 3 model classify the document."""
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": document["title"]},
            ],
            "format": "json",  # Enforces valid JSON
            "stream": False,
            "options": {"temperature": 0},
        },
        timeout=120,
    )
    response.raise_for_status()
    return validate_analysis(json.loads(response.json()["message"]["content"]))


def analyze_demo(document):
    """Simple keyword rules as a fallback when no LLM is available."""
    title = document["title"].lower()
    if "clinical" in title or "health data" in title:
        return {
            "category": "Clinical Trials Transparency",
            "relevance": "high",
            "summary": "The document concerns disclosure obligations for clinical trial and health data.",
            "actions": ["Align positions with industry associations (EFPIA)", "Prepare a technical briefing"],
        }
    if "medical device" in title:
        return {
            "category": "Medical Device Compliance",
            "relevance": "medium",
            "summary": "The document updates technical standards under the MDR.",
            "actions": ["Review internal QM processes against the new standards"],
        }
    return {
        "category": "Not relevant",
        "relevance": "low",
        "summary": "No direct impact on the pharma sector identified.",
        "actions": [],
    }


def validate_analysis(result):
    """Validates the LLM response instead of trusting it blindly."""
    if result.get("category") not in CATEGORIES:
        raise ValueError(f"Unknown category: {result.get('category')!r}")
    if result.get("relevance") not in RELEVANCE:
        raise ValueError(f"Unknown relevance: {result.get('relevance')!r}")
    return {
        "category": result["category"],
        "relevance": result["relevance"],
        "summary": str(result.get("summary", "")),
        "actions": [str(m) for m in result.get("actions", [])],
    }


def analyze_documents(documents, demo):
    results = []
    for doc in documents:
        print(f"🤖 Analyzing: {doc['title'][:70]}")
        try:
            analysis = analyze_demo(doc) if demo else analyze_with_ollama(doc)
        except Exception as e:
            print(f"   ⚠️  Analysis failed: {e}")
            continue
        results.append({**doc, **analysis})
    return results


# OUTPUT: HTML DASHBOARD

BADGES = {"high": "🚨 High", "medium": "⚠️ Medium", "low": "🟢 Low"}

CSS = """
:root { --primary: #2c3e50; --danger: #d9534f; --success: #5cb85c; --bg: #f4f6f8; --card-bg: #fff; --text: #333; }
body { font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: var(--text); background: var(--bg); margin: 0; }
header { background: var(--primary); color: #fff; padding: 20px 40px; }
header h1 { margin: 0; font-size: 22px; }
header p { margin: 4px 0 0; font-size: 13px; opacity: 0.8; }
main { max-width: 900px; margin: 30px auto; padding: 0 16px; }
.notice { background: #fef0de; color: #b97513; padding: 10px 16px; border-radius: 4px; margin-bottom: 20px; font-size: 14px; }
.card { background: var(--card-bg); padding: 25px; border-radius: 6px; box-shadow: 0 4px 10px rgba(0,0,0,0.04); margin-bottom: 25px; border-top: 4px solid var(--primary); }
.card h2 { font-size: 17px; color: var(--primary); margin: 0 0 15px; }
.meta-table { width: 100%; border-collapse: collapse; margin-bottom: 15px; font-size: 14px; }
.meta-table td { padding: 8px 0; border-bottom: 1px solid #f4f4f4; }
.meta-table td:first-child { font-weight: bold; color: #777; width: 25%; }
.badge { display: inline-block; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 12px; }
.high { background: #fdd9d7; color: var(--danger); }
.medium { background: #fef0de; color: #b97513; }
.low { background: #dff0d8; color: var(--success); }
.analysis { background: #fffdf5; border: 1px solid #f0e6c4; padding: 16px 20px; border-radius: 4px; font-size: 14px; }
.btn { color: var(--primary); font-weight: bold; }
"""


def render_card(item):
    e = html.escape  # Escape all text from the feed and the LLM
    actions = "".join(f"<li>{e(m)}</li>" for m in item["actions"])
    link = f'<p><a class="btn" href="{e(item["link"])}" target="_blank" rel="noopener">Open document on EUR-Lex ↗</a></p>' if item["link"] else ""
    return f"""
    <div class="card">
      <h2>{e(item["title"])}</h2>
      <table class="meta-table">
        <tr><td>Category</td><td>{e(item["category"])}</td></tr>
        <tr><td>Relevance</td><td><span class="badge {item["relevance"]}">{BADGES[item["relevance"]]}</span></td></tr>
        <tr><td>Date</td><td>{e(item["date"])}</td></tr>
      </table>
      <div class="analysis">
        <p>{e(item["summary"])}</p>
        {f"<strong>Recommended actions:</strong><ol>{actions}</ol>" if actions else ""}
      </div>
      {link}
    </div>"""


def build_dashboard(results, output_file, notices):
    order = {r: i for i, r in enumerate(RELEVANCE)}
    results = sorted(results, key=lambda r: order[r["relevance"]])

    notice = "".join(f'<div class="notice">{html.escape(n)}</div>' for n in notices)
    cards = "".join(render_card(r) for r in results) or "<p>No relevant documents found.</p>"

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>EU Pharma Regulation Monitor</title>
  <style>{CSS}</style>
</head>
<body>
  <header>
    <h1>EU Pharma Regulation Monitor</h1>
    <p>Updated: {datetime.now():%Y-%m-%d %H:%M}</p>
  </header>
  <main>{notice}{cards}</main>
</body>
</html>"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"🖥️  Dashboard saved: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Monitors EUR-Lex for pharma-relevant EU legislation.")
    parser.add_argument("--demo", action="store_true", help="Run with rule-based analysis instead of Ollama")
    parser.add_argument("--output", default="dashboard.html", help="Path of the HTML output")
    args = parser.parse_args()

    documents, sample_data = fetch_eu_pharma_documents()
    results = analyze_documents(documents, args.demo)

    notices = []
    if sample_data:
        notices.append("Sample data: no EUR-Lex feed was loaded.")
    if args.demo:
        notices.append("Demo mode: rule-based analysis instead of LLM.")
    build_dashboard(results, args.output, notices)


if __name__ == "__main__":
    main()
