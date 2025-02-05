import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(company, days=3, num_results=10):
    """Fetches recent business and financial news for a given company."""
    date_from = (datetime.date.today() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")

    # Improve search by adding financial keywords
    search_query = f'"{company}" AND (earnings OR revenue OR stock OR business OR financial OR market OR profit OR loss OR shares OR investor OR acquisition OR CEO)'

    # Use `domains` to limit sources to business-focused sites
    business_domains = "reuters.com, bloomberg.com, cnbc.com, forbes.com, marketwatch.com, wsj.com, businessinsider.com, finance.yahoo.com"

    url = f"https://newsapi.org/v2/everything?q={search_query}&from={date_from}&sortBy=publishedAt&pageSize={num_results}&domains={business_domains}&apiKey={NEWS_API_KEY}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"NewsAPI error: {response.text}")
        return []
    
    return response.json().get("articles", [])
