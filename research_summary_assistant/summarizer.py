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

def synthesize_research(articles, topic):
    # Build a combined text block with source labels
    combined = ""
    for i, article in enumerate(articles):
        combined += f"\n--- SOURCE {i+1}: {article['url']} ---\n"
        combined += article["text"]
        combined += "\n"

    prompt = PromptTemplate(
        input_variables=["combined", "topic"],
        template="""
You are an expert research analyst. You have been given content from multiple sources on the topic: {topic}

Your job is to synthesize all sources into one unified research report.

{combined}

Respond in this exact format:

RESEARCH REPORT: {topic}

EXECUTIVE SUMMARY:
2-3 sentences capturing the most important overall finding across all sources.

KEY INSIGHTS:
- Insight 1 (mention which source if relevant)
- Insight 2
- Insight 3
- Insight 4
- Insight 5

POINTS OF AGREEMENT:
What do all/most sources agree on?

INTERESTING DIFFERENCES:
Did any sources contradict or add unique perspectives? mention them.

SIMPLE EXPLANATION:
Explain the whole topic in 3 sentences for a complete beginner.

KEY TERMS:
- Term: definition
- Term: definition
- Term: definition

SOURCES USED:
List all source URLs
"""
    )

    chain = prompt | llm
    result = chain.invoke({"combined": combined, "topic": topic})
    return result.content