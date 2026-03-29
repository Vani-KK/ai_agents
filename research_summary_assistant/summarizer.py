from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

def summarize_text(text, topic, source_url):
    prompt = PromptTemplate(
        input_variables=["text", "topic", "source_url"],
        template="""
You are an expert research assistant helping a student understand academic and technical topics.

The user is researching: {topic}
Source: {source_url}

Your job is to read the article below and extract the most useful information.

Respond in this exact format:

TOPIC RELEVANCE:
One sentence on how relevant this article is to "{topic}".

KEY FINDINGS:
- Finding 1
- Finding 2
- Finding 3
- Finding 4
- Finding 5

SIMPLE EXPLANATION:
Explain the core idea in 2-3 sentences as if explaining to a smart 16-year-old.

IMPORTANT TERMS:
List 3-5 technical terms from the article with one-line definitions.

ARTICLE:
{text}
"""
    )

    chain = prompt | llm
    result = chain.invoke({"text": text, "topic": topic, "source_url": source_url})
    return result.content