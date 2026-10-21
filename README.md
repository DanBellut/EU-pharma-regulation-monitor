An automated Python project that collects real-time public data from European legislative databases and filters them into high-relevance regulatory impact categories using a local LLM.
Instead of manually scrolling through extensive legal texts and official journals, this tool automatically scans public draft laws on EUR-Lex, focuses on critical healthcare policy shifts, and displays them inside a clean, live dashboard.
Features 
Data Mining Hub: Simulates and processes live public document streams from the official EUR-Lex RSS repository based on custom keyword routing for European healthcare.
AI Classification: Uses a local LLM (Ollama/Llama 3) to filter out unrelated bureaucratic noise, ensuring legislative changes are strictly categorized into three distinct pharma sectors: Clinical Trials Transparency, Intellectual Property & Patents, and Medical Device Compliance.
Automated Synthesis: Generates rapid, low-latency Public Affairs action points in English to provide an immediate strategic overview of regulatory risks as they happen.
Privacy-First Blueprint: Operates completely in-memory with zero persistent cookie tracking or stored government session files, keeping credential handling safe for local deployment.
Built for Scaling: Cleanly decoupled frontend and backend architecture, designed to easily integrate persistent relational databases (SQLite) and enterprise-grade scraping layers for global health authorities in the future.
Tech Stack Language
Python 3.10+ Interface: Streamlit Legal Mining: BeautifulSoup4 / Requests AI Processing: Ollama (Llama 3)
