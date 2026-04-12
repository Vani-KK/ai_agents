from langchain.tools import tool
from ddgs import DDGS
import wikipedia
from memory import save_memory, get_all_memories, get_memory


@tool
def search_web(query: str) -> str:
    """
    Search the web for current information.
    Use this tool when you need up to date information,
    recent news, or anything that requires live web data.
    Input should be a search query string.
    """
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)
            if not results:
                return "No results found."
            
            # Format results into readable text
            formatted = ""
            for r in results:
                formatted += f"Title: {r['title']}\n"
                formatted += f"Summary: {r['body']}\n"
                formatted += f"URL: {r['href']}\n\n"
            
            return formatted
    except Exception as e:
        return f"Search failed: {str(e)}"
    
@tool
def search_wikipedia(query: str) -> str:
    """
    Search Wikipedia for factual information about a topic.
    Use this tool when you need background knowledge, 
    historical facts, definitions, or general information
    about people, places, concepts, or events.
    Input should be the topic you want to look up.
    """
    try:
        # search() finds the best matching page first
        # then summary() gets the content
        search_results = wikipedia.search(query)
        
        if not search_results:
            return f"No Wikipedia results found for '{query}'"
        
        # Try the first result
        result = wikipedia.summary(search_results[0], sentences=5)
        return f"Wikipedia article: {search_results[0]}\n\n{result}"
        
    except wikipedia.exceptions.DisambiguationError as e:
        # Try the first disambiguation option
        try:
            result = wikipedia.summary(e.options[0], sentences=5)
            return result
        except:
            return f"Multiple matches found: {e.options[:3]}"
    except Exception as e:
        return f"Wikipedia search failed: {str(e)}"


@tool
def calculator(expression: str) -> str:
    """
    Perform mathematical calculations.
    Use this tool when you need to compute numbers,
    perform arithmetic, calculate percentages, or
    solve any mathematical expression.
    Input should be a valid mathematical expression 
    like '25 * 4' or '100 / 3' or '2 ** 10'.
    """
    try:
        # eval() executes a string as Python code
        # We restrict it to math only for safety
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Calculation failed: {str(e)}"
    

@tool
def remember_fact(fact: str) -> str:
    """
    Save an important fact about the user to long term memory.
    Use this when the user tells you something important like
    their name, location, preferences, or any personal detail
    they might want you to remember in future conversations.
    Input format: 'key: value' for example 'user_name: Rithish'
    or 'user_location: Kerala'
    """
    try:
        # Split "user_name: Rithish" into key and value
        if ":" in fact:
            key, value = fact.split(":", 1)
            save_memory(key.strip(), value.strip())
            return f"Got it! I'll remember that {key.strip()} is {value.strip()}"
        else:
            save_memory(fact, fact)
            return f"Remembered: {fact}"
    except Exception as e:
        return f"Failed to save memory: {str(e)}"

@tool
def recall_memories(query: str) -> str:
    """
    Retrieve facts from long term memory about the user.
    Use this when the user asks about something you should
    remember from previous conversations, like their name,
    preferences, or past interactions.
    Input should be what you want to recall.
    """
    memories = get_all_memories()
    return memories

# Updated tools list with memory tools
tools = [search_web, search_wikipedia, calculator, remember_fact, recall_memories]