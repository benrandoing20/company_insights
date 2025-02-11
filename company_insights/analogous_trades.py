import os
from dotenv import load_dotenv
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain.agents import initialize_agent, Tool
from langchain_ollama import ChatOllama
import yahooquery as yq  # Using yahooquery for stock data
import pandas as pd

# Load environment variables
load_dotenv()

# Set up API key (Ensure you have it set in .env or replace it here)
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

# Initialize Ollama LLaMA 3.2 model
llm = ChatOllama(model="llama3.2", temperature=0)

# Set up Tavily Search API wrapper
search_api = TavilySearchAPIWrapper()
tavily_tool = TavilySearchResults(api_wrapper=search_api)

# Function to fetch stock price movement using yahooquery
def get_stock_data(ticker, period="1mo"):
    """Gets stock price movement for a company using yahooquery over a given period."""
    stock = yq.Ticker(ticker)
    history = stock.history(period=period)

    if not history.empty:
        # Reset index to access 'date' as a column instead of MultiIndex
        history.reset_index(inplace=True)
        return history.to_dict(orient="records")  # Return historical data as a list of dicts
    else:
        return {"error": "Stock data unavailable."}

# Function to search for similar past events
def search_trends(company_event):
    """Uses Tavily API to find similar past events and their financial impact."""
    query = f"Find past company events similar to: {company_event}. Focus on financial impact and the event date."
    return tavily_tool.invoke(query)  # Using TavilySearchResults

# Define LangChain Agent Tools
tools = [
    Tool(name="CompanyTrendSearch", func=search_trends, description="Searches for past similar company events."),
    Tool(name="StockPriceLookup", func=get_stock_data, description="Gets historical stock price movements.")
]

# Initialize LLM Agent with Tools
agent = initialize_agent(
    tools=tools, 
    llm=llm, 
    agent="zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True
)

def analyze_company_highlight(company, event_description, stock_ticker):
    """
    Takes a company highlight (event) and runs LLM research to find past similar events,
    stock price impact, and a synthesized financial analysis.
    """
    print(f"\n **Analyzing Event for {company}**: {event_description}\n")

    # Step 1: Search for similar past events
    past_event_analysis = search_trends(event_description)

    print(past_event_analysis)

    # Extract date if available
    past_event_date = None
    if isinstance(past_event_analysis, list) and len(past_event_analysis) > 0:
        for entry in past_event_analysis:
            if "date" in entry:
                past_event_date = entry["date"]
                break

    # Step 2: Fetch historical stock price movement based on past event date
    stock_price_movement = get_stock_data(stock_ticker)

    print(stock_price_movement)

    if past_event_date:
        print(f"\n Found Similar Event on: {past_event_date}. Fetching stock movement around that date...\n")
        historical_stock_price = get_stock_data(stock_ticker, period="3mo")  # Get stock data for the last 3 months
    else:
        historical_stock_price = "No past event date found."

    print(historical_stock_price)

    # Step 3: Synthesize financial analysis using LLM
    query = f"""
    You are a financial analyst. Given the company **{company}** and the event: **{event_description}**, analyze its potential financial impact.

    **Process:**
    1. Check for similar past events and summarize what happened.
    2. Find the stock price impact from those past events.
    3. Predict how the current event may affect {company} based on historical data.

    **Similar Past Event Analysis:**
    - {past_event_analysis}

    **Stock Price Impact (if event date found: {past_event_date}):**
    - {historical_stock_price}

    Provide a structured report with:
    - Summary of past trends
    - Observed financial impact
    - Predicted impact on {company}
    - Uncertainties and risks to consider
    """

    print(query)

    financial_analysis = agent.invoke(query)

    print(f"\n **Financial Impact Analysis for {company}:**\n")
    print(financial_analysis)
    print(f"\n **Stock Price Movement Today:** {stock_price_movement}")

    return financial_analysis, stock_price_movement

# Example daily highlight for Starbucks
company = "Starbucks"
event = "Starbucks, a consumer food and drink company, announces mass layoffs of around 15,000 people due to rising operational costs."
ticker = "SBUX"

analyze_company_highlight(company, event, ticker)
