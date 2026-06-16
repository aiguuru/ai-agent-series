"""
AI Agent — 40 lines of Python
================================
What it does:
  1. Takes a research goal
  2. Searches the web using Tavily
  3. Summarises the results using GPT-4o
  4. Writes the output to a markdown file

Requirements:
  pip install langchain langchain-openai langchain-community tavily-python

Env vars needed:
  OPENAI_API_KEY   — from platform.openai.com
  TAVILY_API_KEY   — from app.tavily.com (free tier works)
"""

import os, time
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

# ── 1. LLM (Brain) ───────────────────────────────────────────────────────────
llm = ChatOpenAI(
    model="gpt-4o-mini",          # cheap, fast — swap to gpt-4o for better quality
    temperature=0,                 # deterministic for agents
    max_tokens=1000,               # non-functional: cap token cost per call
)

# ── 2. Tool (Search) ─────────────────────────────────────────────────────────
search_tool = TavilySearchResults(
    max_results=3,                 # non-functional: limits API cost + context size
    search_depth="basic",
)
tools = [search_tool]

# ── 3. Prompt (ReAct loop template) ─────────────────────────────────────────
prompt = hub.pull("hwchase17/react")   # standard ReAct prompt from LangChain hub

# ── 4. Agent + Executor ──────────────────────────────────────────────────────
agent        = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,                  # prints each Thought / Action / Observation
    max_iterations=5,              # non-functional: prevents infinite loops
    handle_parsing_errors=True,    # non-functional: recovers from bad LLM output
)

# ── 5. Run + Write output ────────────────────────────────────────────────────
def run_agent(goal: str, output_file: str = "output.md") -> None:
    print(f"\n🎯 Goal: {goal}\n{'─'*50}")

    # Non-functional: retry on rate limit (429) with exponential backoff
    for attempt in range(3):
        try:
            result = agent_executor.invoke({"input": goal})
            break
        except Exception as e:
            if "429" in str(e) and attempt < 2:
                wait = 2 ** attempt * 5        # 5s, 10s, 20s
                print(f"⚠️  Rate limited. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise

    # Write result to markdown file
    with open(output_file, "w") as f:
        f.write(f"# Research: {goal}\n\n")
        f.write(result["output"])

    print(f"\n✅ Done. Output written to {output_file}")
    print(f"💰 Approx cost: ~${len(str(result)) * 0.000002:.4f}")  # rough GPT-4o-mini estimate

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_agent(
        goal="What are the top 3 use cases for AI agents in enterprise software in 2025?",
        output_file="research_output.md"
    )
