import os
from firecrawl import FirecrawlApp

# Load Firecrawl API Key from environment variables
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# Initialize Firecrawl App
app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

def scrape_article(url):
    """
    Scrapes full article content from a given URL using Firecrawl.
    
    Parameters:
        url (str): The URL of the article to scrape.

    Returns:
        str: Scraped article content in markdown format, or an error message.
    """
    try:
        scrape_result = app.scrape_url(url, params={'formats': ['markdown']})
        return f"Result of scrape at {url}: {scrape_result}"
    
    except Exception as e:
        return f"Error scraping {url}: {e}"
