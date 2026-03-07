from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

def summarize_text(text):

    prompt = PromptTemplate(
        input_variables=["text"],
        template="""
You are a research assistant.

Summarize the following article into 5 clear bullet points.

ARTICLE:
{text}
"""
    )

    chain = prompt | llm

    result = chain.invoke({"text": text})

    return result.content