## What This Project Is

This repository contains a Self-Refining AI Agent that:
- takes a clear goal
- generates an initial solution
- evaluates its own output against fixed criteria
- iteratively improves the output
- stops when the goal is met or a safety limit is reached

The agent is implemented without frameworks to make the core ideas behind agentic AI transparent and easy to understand.

## Agent Goal

Given an input text, the agent must produce a summary that:
- is 120 words or fewer
- is beginner-friendly
- is clear and concise
- avoids technical jargon

The agent may refine its output over multiple iterations and must stop when all criteria are met or after a maximum of 5 iterations.


## Why This Is an AI Agent (Not a Chatbot)

Unlike a traditional chatbot, this system:
- pursues a goal rather than answering once
- runs in an explicit reasoning loop
- performs self-evaluation
- decides whether to continue or stop
- operates autonomously after being started

At its core, the agent follows this loop:
Generate → Evaluate → Decide → Refine (or Stop)


## Tech Stack
- Python
- Jupyter Notebook
- OpenAI API

## No agent frameworks are used to ensure full control and learning transparency.
