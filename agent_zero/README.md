## Built my first True AI-Agent

# Agent Zero 

A true AI agent that reasons, decides, and uses tools autonomously to answer questions.
Unlike a simple chatbot, Agent Zero thinks through problems step by step and chooses
the right tool for each task — without being told what to do.



## What Makes This an Agent?

Most AI apps follow fixed steps you define in code. Agent Zero is different:

- You give it a **goal**

- It **decides** which tools to use and when

- It **retries** with different approaches when tools fail

- It **keeps going** until the goal is achieved



## Tools Available

Web Search | Current events, recent news, live data |

Wikipedia | Historical facts, definitions, background knowledge |

Calculator | Mathematical expressions and computation |



## Tech Stack

- **LangGraph** — agent loop and reasoning framework

- **OpenAI GPT-4o-mini** — the brain of the agent

- **DuckDuckGo (ddgs)** — web search

- **Wikipedia API** — factual knowledge

- **Streamlit** — web interface



## Setup

**1. Clone the repo**

git clone https://github.com/Vani-KK/ai_agents.git

cd ai_agents/agent_zero


**2. Create and activate virtual environment**

python -m venv venv

venv\Scripts\activate  # Windows


**3. Install dependencies**

pip install langchain langchain-openai langgraph ddgs wikipedia streamlit python-dotenv


**4. Add your API key**

Create a `.env` file:

OPENAI_API_KEY=your-openai-api-key-here


**5. Run the app**

streamlit run app.py



## Key Concepts Demonstrated

- **ReAct Pattern** — Reason, Act, Observe, Repeat

- **Tool Calling** — LLM decides when and how to use tools

- **Agent Loop** — continues until goal is achieved

- **Error Recovery** — retries with different inputs when tools fail

- **Transparent Reasoning** — view every tool call and result in the UI


