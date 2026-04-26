# Job Application Assistant 💼

A multi-agent AI system that automatically tailors your resume and writes 
a personalized cover letter for any job description. Powered by a team of 
three specialized AI agents working together using CrewAI.



## What Makes This Different?

Unlike asking ChatGPT to write a resume, this system uses three specialized 
agents that each focus on one job — producing expert-level output at every step.
The output of each agent feeds directly into the next, creating a pipeline of
increasingly refined application materials.



## Your AI Team

| Agent | Role | What it does |


| 🔍 Job Analyst | HR Expert | Extracts skills, keywords, culture insights |
| ✍️ Resume Tailor | Professional Resume Writer | Rewrites resume to match job perfectly |
| 📝 Cover Letter Writer | Former Hiring Manager | Writes personalized cover letter |



## Features

- **Dual input methods** — Upload your existing resume as PDF or type manually
- **ATS optimization** — Keywords naturally incorporated to pass screening systems
- **Tabbed results** — Clean separation of analysis, resume, and cover letter
- **Download buttons** — Save all outputs as text files
- **Persistent results** — Results stay visible even after downloading



## Tech Stack

- **CrewAI** — Multi-agent orchestration framework
- **LangChain + OpenAI GPT-4o-mini** — LLM powering each agent
- **Streamlit** — Web interface
- **pypdf** — PDF text extraction



## How to Use

1. Paste any job description in the sidebar
2. Either upload your resume PDF or type your background manually
3. Click **Generate Application Materials**
4. Wait 1-2 minutes while the AI team works
5. Switch between tabs to view Job Analysis, Resume, and Cover Letter
6. Download any or all outputs



## Key Concepts Demonstrated

- **Multi-agent systems** — specialized agents outperform single agents on complex tasks
- **Sequential processing** — each agent's output becomes the next agent's input
- **Role and backstory** — agent personas shape output quality and depth
- **ATS optimization** — real-world resume engineering techniques
- **PDF extraction** — reading and processing uploaded documents
- **Session state** — persisting results across Streamlit reruns

