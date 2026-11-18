# ResearchMind

An AI-powered multi-agent research assistant built with Python, Streamlit, LangChain, LangGraph-compatible agent tooling, Groq, and Tavily. ResearchMind searches the web, extracts relevant page content, drafts a structured research report, and reviews the report with a critic stage.

## Features

- **Search Agent:** discovers recent information using Tavily.
- **Reader Agent:** extracts readable content from selected webpages.
- **Writer:** creates a structured research report.
- **Critic:** evaluates the generated report and provides improvement feedback.
- **Streamlit UI:** interactive dark interface with animated pipeline status and Markdown report download.

## Architecture

```text
ResearchMind/
├── app.py             # Streamlit application
├── agents.py          # LLM configuration and agent/report chains
├── tools.py           # Tavily search and webpage scraping tools
├── pipeline.py        # Command-line research pipeline
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variable template
└── .gitignore         # Excludes secrets and local files
```

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows PowerShell
   .venv\\Scripts\\Activate.ps1
   # macOS/Linux
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a local `.env` file from the template and add your own API keys:

   ```env
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

4. Start the app:

   ```bash
   streamlit run app.py
   ```

## Run the pipeline from the terminal

   ```bash
   python pipeline.py
   ```

## Security

Keep API keys in your local `.env` file or deployment secrets. Never commit credentials, virtual environments, or Streamlit secrets. The real `.env` file is excluded by `.gitignore`.

## Tech Stack

Python · Streamlit · LangChain · Groq · Tavily · Requests · BeautifulSoup
