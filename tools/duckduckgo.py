from langchain.tools import tool
from duckduckgo_search import DDGS

@tool("duckduckgo_search", return_direct=True)
def duckduckgo_search_tool(query: str) -> str:
    """
    Perform a web search using DuckDuckGo and return top results with summaries.
    Use this tool when the user asks a question that requires up-to-date information from the internet.
    
    Examples of queries:
    - "Please look up what's the weather like in Paris today?"
    - "Look up the latest tech news"
    - "yes, please search for current AI news"

    Input:
    - A natural language query string.
    """
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, region='wt-wt', safesearch='Moderate', max_results=3)
            results_list = list(results)

        if not results_list:
            return f"I couldn't find any results for: \"{query}\"."

        # Format top 3 results with snippets
        response = f"Here's what I found for \"{query}\":\n\n"
        
        for i, result in enumerate(results_list[:3], 1):
            response += f"{i}. {result['title']}\n"
            response += f"   {result.get('body', 'No description available.')}\n"
            if i < len(results_list):
                response += "\n"
        
        return response
    
    except Exception as e:
        return f"Search error: {str(e)}"
