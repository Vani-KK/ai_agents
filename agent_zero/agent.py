# import os
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain.agents import create_react_agent
# from langchain_core.agents import AgentExecutor
# from langchain.prompts import PromptTemplate
# from tools import tools

# load_dotenv()

# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0  # temperature 0 = focused, consistent reasoning
# )

# react_prompt = PromptTemplate.from_template("""
# You are a smart AI assistant that can use tools to answer questions.
# You have access to the following tools:

# {tools}

# To answer the user's question, use this exact format:

# Thought: Think about what you need to do
# Action: the tool name to use (must be one of [{tool_names}])
# Action Input: the input to pass to the tool
# Observation: the result returned by the tool

# Repeat Thought/Action/Action Input/Observation as many times as needed.
# When you have enough information to answer, use:

# Thought: I now have enough information to answer
# Final Answer: your complete answer here

# Begin!

# Question: {input}
# Thought: {agent_scratchpad}
# """)

# def run_agent(user_input: str) -> dict:
#     # Step 1: Create the agent
#     # This combines the LLM + tools + prompt into one reasoning unit
#     agent = create_react_agent(
#         llm=llm,
#         tools=tools,
#         prompt=react_prompt
#     )
    
#     # Step 2: Create the executor
#     # This is what actually runs the agent loop
#     executor = AgentExecutor(
#         agent=agent,
#         tools=tools,
#         verbose=True,        # prints every thought/action to terminal
#         max_iterations=5,    # safety limit - stops after 5 loops
#         handle_parsing_errors=True  # recovers gracefully from LLM formatting errors
#     )
    
#     # Step 3: Run it with the user's input
#     result = executor.invoke({"input": user_input})
    
#     return result

# if __name__ == "__main__":
#     print("Agent Zero - Ready")
#     print("Type 'quit' to exit\n")
    
#     while True:
#         user_input = input("You: ")
        
#         if user_input.lower() == "quit":
#             break
            
#         if user_input.strip() == "":
#             continue
        
#         print("\nThinking...\n")
#         result = run_agent(user_input)
#         print(f"\nFinal Answer: {result['output']}\n")
#         print("-" * 50)




import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from tools import tools
from memory import get_all_memories

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

agent = create_react_agent(
    model=llm,
    tools=tools
)

def run_agent(user_input: str, chat_history: list = []) -> dict:
    
    # Load existing long term memories
    long_term = get_all_memories()
    
    # System message tells agent who the user is before conversation starts
    system_message = SystemMessage(content=f"""
You are Agent Zero, a helpful AI assistant with memory capabilities.

You have access to tools for web search, wikipedia, calculator, 
and memory storage.

IMPORTANT MEMORY INSTRUCTIONS:
- If the user tells you their name, location, or any personal detail → 
  use remember_fact tool to save it immediately
- If the user asks about something from previous conversations → 
  use recall_memories tool first
- Always be personal and use the user's name if you know it

WHAT YOU ALREADY KNOW ABOUT THIS USER:
{long_term}
""")
    
    # Combine system message + chat history + new message
    messages = [system_message] + chat_history + [
        {"role": "user", "content": user_input}
    ]
    
    result = agent.invoke({"messages": messages})
    
    # Extract steps for UI display
    steps = []
    for message in result["messages"]:
        if hasattr(message, 'tool_calls') and message.tool_calls:
            for tool_call in message.tool_calls:
                steps.append({
                    "type": "tool_call",
                    "tool": tool_call['name'],
                    "input": tool_call['args']
                })
        elif hasattr(message, 'name') and message.name:
            steps.append({
                "type": "tool_result",
                "tool": message.name,
                "output": message.content[:200]
            })
    
    return {
        "answer": result["messages"][-1].content,
        "steps": steps
    }
