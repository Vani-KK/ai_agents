from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

def answer_question(question, chunks , sources):
    
    # Join all chunks into one context block
    context = "\n\n---\n\n".join(chunks)
    sources_text = ", ".join(sources)
    
    prompt = PromptTemplate(
        input_variables=["context", "question", "sources"],
        template="""
You are a helpful assistant that answers questions based on the provided context.
Use the context as your source of truth, but explain the answer in a clear, 
natural, and conversational way. Don't copy sentences directly — understand 
the content and explain it in your own words.
If the answer is not found in the context, say "I couldn't find that in the document."
Do NOT make up answers or use outside knowledge.

SOURCES: {sources}
CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""
    )
    
    chain = prompt | llm
    result = chain.invoke({"context": context, "question": question, "sources": sources_text})
    return result.content