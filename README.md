# AI Agent — 40 Lines of Python

A working ReAct agent that searches the web, summarises results, and writes to a file.

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API keys
cp .env.example .env
# Edit .env with your keys

# 3. Run
python agent.py
```

## Get API Keys
- **OpenAI**: https://platform.openai.com/api-keys
- **Tavily** (free tier): https://app.tavily.com

## What it demonstrates
- Functional: tool use, ReAct loop, output parsing, file writing
- Non-functional: max_iterations cap, retry with exponential backoff, token cost control
