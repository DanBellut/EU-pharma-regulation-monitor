++++EU Pharma Regulation Monitor+++

A Python tool that scans EUR-Lex for new EU legislation relevant to the pharma sector, classifies each document with a local LLM and creates an HTML dashboard with prioritized Public Affairs recommendations.

Status
Early prototype.

Features
EUR-Lex monitoring:Reads an EUR-Lex RSS feed and keeps only documents that match healthcare keywords such as "medicinal", "clinical" or "medical device".
Uses Llama 3 via Ollama in JSON mode with `temperature=0` to sort each document into Clinical Trials Transparency, Intellectual Property & Patents or Medical Device Compliance. No data leaves your machine.
Output validation: Categories and relevance levels outside the allowed lists are rejected instead of silently entering the dashboard.
Actionable briefings: Each document gets a relevance rating (high / medium / low), a short summary and recommended Public Affairs actions.
HTML dashboard: Results are rendered as a static web page, sorted by relevance, with all text from the feed and the LLM safely escaped.
Demo mode: Runs without Ollama using rule-based analysis, and the dashboard clearly marks when sample data or demo mode is used.
Roadmap

Streamlit interface · SQLite storage · analysis of full legal texts · additional health authorities
