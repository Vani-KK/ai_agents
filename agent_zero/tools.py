from langchain.tools import tool
from ddgs import DDGS
import wikipedia

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
    
tools = [search_web, search_wikipedia, calculator]

