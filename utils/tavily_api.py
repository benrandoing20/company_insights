import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

def fetch_tavily_results(query):
    """Fetches Tavily search results for a given company."""
    try:
        results = tavily_client.search(query=query)
        return results.get("results", [])
    except Exception as e:
        print(f"Error querying Tavily: {e}")
        return []
