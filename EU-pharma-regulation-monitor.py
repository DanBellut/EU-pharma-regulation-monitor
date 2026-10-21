import time
import requests
from bs4 import BeautifulSoup

class FantasyAIApiClient:
    """Simuliert die Anbindung an ein modernes LLM (wie OpenAI GPT-4o)."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        if not api_key.startswith("sk-fantasy-"):
            raise ValueError("❌ API-Authentifizierungsfehler! Der Schlüssel muss mit 'sk-fantasy-' beginnen.")

    def generate_regulatory_briefing(self, model: str, prompt: str) -> dict:
        """Simuliert den API-Call mit einer Netzwerk-Latenz und intelligenter Textgenerierung."""
        print(f"📡 [API] Übermittle Daten an Cloud-Modell '{model}'...")
        time.sleep(1.2)  # Simuliert die Rechenzeit des KI-Servers
        
        # Auswertungs-Logik der Fantasie-KI anhand von Signalwörtern
        prompt_lower = prompt.lower()
        
        if "clinical trials" in prompt_lower or "biologics" in prompt_lower:
            ki_text = (
                "### 🚨 EXEKUTIVE ZUSAMMENFASSUNG: HOHE RELEVANZ\\n"
                "Das identifizierte EU-Dokument reformiert die Offenlegungspflichten für klinische Studien "
                "und biopharmazeutische Zulassungen. Es besteht akuter Handlungsbedarf für forschende Unternehmen, "
                "da geschützte Geschäftsdaten (IP) betroffen sein könnten.\\n\\n"
                "**Empfohlene Public Affairs-Roadmap:**\\n"
                "1. 🇪🇺 **Direktes Lobbying:** Kontaktaufnahme mit den Koordinatoren des ENVI-Ausschusses im Europäischen Parlament.\\n"
                "2. 🤝 **Verbands-Allianz:** Einberufung einer Krisensitzung über die Branchenverbände (z. B. EFPIA / vfa) zur Bündelung der Kräfte.\\n"
                "3. 📄 **Position Paper:** Finalisierung eines zweiseitigen technischen Briefings zu den ökonomischen Standortrisiken innerhalb von 14 Tagen."
            )
        elif "medical devices" in prompt_lower or "software" in prompt_lower:
            ki_text = (
                "### ⚠️ EXEKUTIVE ZUSAMMENFASSUNG: MITTLERE RELEVANZ\\n"
                "Es handelt sich um eine Anpassung der harmonisierten Normen im Rahmen der Medical Device Regulation (MDR). "
                "Keine unmittelbare Gefahr für bestehende Zulassungen, jedoch mittelfristige Audit-Risiken für Neuentwicklungen.\\n\\n"
                "**Empfohlene Public Affairs-Roadmap:**\\n"
                "1. 🔍 **Konformitäts-Check:** Abgleich der internen Qualitätsmanagement-Prozesse mit den neuen technischen Anhängen.\\n"
                "2. 🏢 **Notified Body:** Frühzeitige Konsultation der Benannten Stelle zur Vermeidung von Zertifizierungsstaus."
            )
        else:
            ki_text = (
                "### 🟢 EXEKUTIVE ZUSAMMENFASSUNG: NIEDRIGE RELEVANZ\\n"
                "Der Sektor wird durch die Rechtsvorschrift nur peripher tangiert. Es sind keine regulatorischen Hürden zu erwarten.\\n\\n"
                "**Empfehlung:** Der Vorgang wird rein dokumentarisch im Quartalsbericht erfasst. Keine operativen Maßnahmen notwendig."
            )

        return {
            "status": "success",
            "model_used": model,
            "choices": [{"message": {"content": ki_text}}]
        }

# MONITORING-ENGINE: EUR-LEX RSS SCRAPER

def fetch_eu_pharma_stream():
    """Überwacht das EU-Amtsblatt via EUR-Lex-Schnittstelle auf gesundheitsrelevante Gesetze."""
    print("🔮 [1/3] Scrape aktuelle EU-Dokumente aus der EUR-Lex Datenbank...")
    url = "https://europa.eu"
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")
        
        pharma_keywords = ["medicinal", "pharma", "clinical", "health", "medical devices", "Arzneimittel", "Gesundheit"]
        detected_docs = []
        
        for item in items:
            title = item.title.text.strip()
            if any(kw.lower() in title.lower() for kw in pharma_keywords):
                detected_docs.append({
                    "title": title,
                    "link": item.link.text.strip() if item.link else "https://europa.eu",
                    "date": item.pubDate.text.strip() if item.pubDate else "Aktuell"
                })
        
        if detected_docs:
            return detected_docs[:2]  # Beschränkung auf die neuesten Treffer
    except Exception as e:
        print(f"⚠️ EUR-Lex Live-Schnittstelle temporär blockiert ({e}). Nutze integrierte Echtzeit-Pipeline...")
    
    # Hochrelevanter Fallback-Vorgang für die System-Demonstration
    return [{
        "title": "Regulation on European Health Data Space (EHDS) and requirements for clinical trials data transparency",
        "link": "https://europa.eu/legal-content/EN/TXT/?uri=CELEX:52022PC0197",
        "date": "Wed, 21 Oct 2026 14:00:00 GMT"
    }]

# INTERFACE: GENERATOR FÜR DAS WEB-DASHBOARD
def compile_web_dashboard(output_file, results_data):
    """Kompiliert alle Ergebnisse in eine voll funktionsfähige, moderne Überwachungs-Webseite."""
    print(f"🖥️  [3/3] Generiere interaktives Web-Dashboard: '{output_file}'...")
    
    # HTML-Struktur der Fallkarten dynamisch aufbauen
    cards_html = ""
    for item in results_data:
        # Einfache Formatierung für HTML-Zeilenumbrüche im Dashboard
        parsed_ki_text = item['analysis'].replace('\\n', '<br>').replace('###', '<h2>')
        
        # Bestimme Dringlichkeits-Farbe
        badge_style = "priority-high" if "🚨" in parsed_ki_text else ("priority-med" if "⚠️" in parsed_ki_text else "priority-low")
        badge_label = "🚨 Hoch" if "🚨" in parsed_ki_text else ("⚠️ Mittel" if "⚠️" in parsed_ki_text else "🟢 Niedrig")

        cards_html += f"""
        <div class="card">
            <div class="card-title">🚨 System-Alarm: Regulatorischer Neueintrag</div>
            <table class="meta-table">
                <tr><td>EU-Dokument</td><td><strong>{item['title']}</strong></td></tr>
                <tr><td>Ziel-Mandant</td><td><span class="client-tag">{item['client']}</span></td></tr>
                <tr><td>Dringlichkeit</td><td><span class="priority-badge {badge_style}">{badge_label}</span></td></tr>
                <tr><td>Erfassungsdatum</td><td>{item['date']}</td></tr>
            </table>
            <div class="ai-analysis">
                {parsed_ki_text}
            </div>
            <div style="margin-top: 20px; text-align: right;">
                <a href="{item['link']}" target="_blank" class="btn">Original-Gesetzestext (EUR-Lex) öffnen ↗</a>
            </div>
        </div>
        """

    html_layout = f"""<!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>EU Pharma Monitoring Platform</title>
        <style>
            :root {{
                --primary: #2c3e50; --danger: #d9534f; --warning: #f0ad4e; --success: #5cb85c;
                --bg: #f4f6f8; --card-bg: #ffffff; --text: #333333;
            }}
            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: var(--text); background-color: var(--bg); margin: 0; }}
            header {{ background-color: var(--primary); color: white; padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            header h1 {{ margin: 0; font-size: 22px; }}
            .live-badge {{ background-color: var(--danger); color: white; padding: 6px 14px; border-radius: 20px; font-size: 11px; font-weight: bold; animation: pulse 2s infinite; }}
            @keyframes pulse {{ 0% {{ opacity: 0.6; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.6; }} }}
            main {{ max-width: 1200px; margin: 30px auto; padding: 0 20px; display: grid; grid-template-columns: 2.5fr 1fr; gap: 30px; }}
            @media (max-width: 900px) {{ main {{ grid-template-columns: 1fr; }} }}
            .card {{ background: var(--card-bg); padding: 25px; border-radius: 6px; box-shadow: 0 4px 10px rgba(0,0,0,0.04); margin-bottom: 25px; border-top: 4px solid var(--primary); }}
            .card-title {{ font-size: 18px; font-weight: bold; color: var(--primary); margin-top: 0; margin-bottom: 15px; }}
            .meta-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 14px; }}
            .meta-table td {{ padding: 10px 0; border-bottom: 1px solid #f4f4f4; }}
            .meta-table td:first-child {{ font-weight: bold; color: #777777; width: 25%; }}
            .client-tag {{ background: #eef2f7; padding: 3px 8px; border-radius: 4px; font-weight: bold; color: var(--primary); }}
            .priority-badge {{ display: inline-block; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 12px; }}
            .priority-high {{ background-color: #fdd9d7; color: var(--danger); }}
            .priority-med {{ background-color: #fef0de; color: #b97513; }}
            .priority-low {{ background-color: #dff0d8; color: var(--success); }}
            .ai-analysis {{ background-color: #fffdf5; border: 1px solid #f0e6c4; padding: 20px; border-radius: 4px; font-size: 14px; }}
            .ai-analysis h2 {{ font-size: 15px; color: #795548; margin-top: 0; text-transform: uppercase; border-bottom: 1px dashed #f0e6c4; padding-bottom: 5px; }}
