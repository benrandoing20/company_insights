import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import re
import pandas as pd
from collections import defaultdict

# For the LLM
from langchain_ollama import ChatOllama

# For Tavily Search
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_community.tools.tavily_search.tool import TavilySearchResults

import yahooquery as yq

load_dotenv()
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

llm = ChatOllama(model="llama3.2")

# 3) Initialize Tavily Search
search_api = TavilySearchAPIWrapper()
tavily_tool = TavilySearchResults(api_wrapper=search_api)


# ---------------------------------------------------------------------------- #
#                        Identify Similar Companies/Events                     #
# ---------------------------------------------------------------------------- #
def search_similar_companies_and_events(company_event_description, max_competitors=3):
    """
    1) Ask the LLM to propose competitor companies that experienced a similar event.
    2) For each proposed competitor event, call Tavily to gather historical context.

    Returns a list of dicts, each containing:
      {
        'competitor': <company name>,
        'reasoning': <short reason from LLM>,
        'event_date': <parsed event date from llm reasoning>
      }
    """
    # ---------------------- Step 1: LLM to find competitor companies  ---------------------- #
    prompt_competitors = f"""
    You are a market analyst. The company event is:
    "{company_event_description}"

    Identify up to {max_competitors} competitor companies in the same industry that had a similar event.
    Provide reasoning for each competitor.

    STRICT RULES:
    - **RETURN ONLY VALID JSON** (No extra text).
    - **NO INTRODUCTION OR EXPLANATION**.
    - Use this exact JSON structure:
    [{{"competitor": "<company name>", "reasoning": "<detailed reason of the similar event and what happened to the company's stock as a resultt of it, provide a very specific date Year Month Day of when the event happened>"}}]
    """

    llm_response = llm.invoke(prompt_competitors)

    # Parse the response (assume well-formed JSON, but be prepared for fallback)

    competitor_info = extract_competitor_info(llm_response.content)
    print(competitor_info)

    if not isinstance(competitor_info, list):
        competitor_info = []

    # ---------------------- Step 2: For each competitor, identify the date of what happened ---------------------- #
    results = []
    for item in competitor_info:
        competitor = item.get("competitor", "")
        reasoning = item.get("reasoning", "")
        if not competitor:
            continue

        query = f"Historical details about {competitor} having a similar event to: {reasoning}. Focus on date and financial impact."

        event_date = infer_event_date_with_llm(query)

        results.append(
            {"competitor": competitor, "reasoning": reasoning, "event_date": event_date}
        )

        print(results)

    return results


# ---------------------------------------------------------------------------- #
#                   B) Retrieve Stock Data Around a Given Date                 #
# ---------------------------------------------------------------------------- #
def get_stock_data_for_event(ticker, event_date_str, days_before=30, days_after=30):
    """
    Given a ticker and an event_date_str (YYYY-MM-DD), retrieve stock data from
    (event_date - days_before) to (event_date + days_after) via yahooquery.

    Returns a list of dicts with price data. If event_date is None/invalid,
    returns an error dict.
    """
    if not event_date_str:
        return {"error": "No valid event date provided. Cannot fetch stock data."}

    try:
        event_date = datetime.fromisoformat(event_date_str)
    except ValueError:
        return {"error": f"Invalid event date format: {event_date_str}"}

    start_date = (event_date - timedelta(days=days_before)).strftime("%Y-%m-%d")
    end_date = (event_date + timedelta(days=days_after)).strftime("%Y-%m-%d")

    stock = yq.Ticker(ticker)
    # yahooquery's 'history' can accept start and end date
    history = stock.history(start=start_date, end=end_date)

    if history.empty:
        return {
            "error": f"No stock data found for {ticker} between {start_date} and {end_date}."
        }

    history.reset_index(inplace=True)
    print(history.to_dict(orient="records"))
    return history.to_dict(orient="records")


# ---------------------------------------------------------------------------- #
#                    C) Main Analysis Orchestration Function                   #
# ---------------------------------------------------------------------------- #
def analyze_company_highlight(company, event_description, ticker):
    """
    1. Use an LLM to find competitor companies that had a similar event.
    3. Fetch stock price data around that date ideentified.
    4. Finally, use the LLM once more to synthesize all of this information into a
       coherent financial analysis.

    Returns:
        final_analysis (str): The LLM-generated report.
        competitor_info (list): Detailed info about competitor events & stock data.
    """

    print(
        f"\n=== Analyzing Event for {company} ===\nEvent Description: {event_description}\n"
    )

    # ------------------------------------------------ #
    #  Step 1: Identify Similar Companies and Events   #
    # ------------------------------------------------ #
    competitor_events = search_similar_companies_and_events(
        event_description, max_competitors=3
    )
    print("\n--- Similar Company Events (from LLM + Tavily) ---")
    for ce in competitor_events:
        print(
            f"* Competitor: {ce['competitor']}\n  Reason: {ce['reasoning']}\n  Event Date: {ce['event_date']}"
        )

    # ------------------------------------------------ #
    #  Step 2: Fetch Stock Data for the Discovered Date
    # ------------------------------------------------ #
    # Store extended info in a new field
    for ce in competitor_events:
        event_date = ce["event_date"]
        # Example: if we found a date, fetch stock data ~1mo before, 1mo after
        stock_data = get_stock_data_for_event(
            ticker, event_date, days_before=30, days_after=30
        )
        parsed_insights = parse_stock_data(
            stock_data
        )  # Assuming stock_data is provided
        print(parsed_insights)
        ce["stock_data"] = parsed_insights

    # ------------------------------------------------ #
    #  Step 3: Synthesize Everything via LLM
    # ------------------------------------------------ #
    # Format a prompt that references the competitor info, event date, and stock data
    competitor_summaries = []
    for ce in competitor_events:
        competitor_summaries.append(
            f"""
                Competitor: {ce["competitor"]}
                Event Date: {ce["event_date"]}
                Reasoning: {ce["reasoning"]}
                Stock Data: {ce["stock_data"]}
            """
        )

    final_prompt = f"""
        You are a financial analyst. A major event has occurred for {company}: 
        "{event_description}"

        We identified some competitor events and historical data:

        {"".join(competitor_summaries)}

        Please provide a structured financial analysis:
        1. Analyze the financial data above and outline your summary of the stock progress for each company. 
        1. Summarize what happened in the anlagous companies stock as a result of the similar events.
        3. Analysis of what might happen with {company}'s stock or finances given these historical parallels.
        4. Mention key uncertainties or caveats.

        Provide your answer in a concise, professional tone.
    """

    print("\n--- Final LLM Prompt ---")
    print(final_prompt)
    print("\n--- Generating Final Analysis ---")

    final_analysis = llm.invoke(final_prompt)
    print(f"\n=== Final Analysis ===\n{final_analysis}")

    return final_analysis, competitor_events


def extract_competitor_info(llm_response_text):
    """
    Extracts competitor names and reasoning from an LLM response string
    that is JSON-like but may not be perfectly formatted.
    """

    # Define a regex pattern to capture competitors and their reasoning
    pattern = r'\{\s*"competitor":\s*"([^"]+)",\s*"reasoning":\s*"([^"]+)"\s*\}'

    matches = re.findall(pattern, llm_response_text)

    # Convert matches into a structured list
    competitors = [
        {"competitor": comp, "reasoning": reason} for comp, reason in matches
    ]

    return competitors


def normalize_date(date_str):
    """
    Converts extracted dates into standardized YYYY-MM-DD format.
    """
    try:
        # If already in YYYY-MM-DD
        if re.match(r"\d{4}-\d{2}-\d{2}", date_str):
            return date_str
        # Convert MM/DD/YYYY
        elif re.match(r"\d{2}/\d{2}/\d{4}", date_str):
            return datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
        # Convert "Month Day, Year" (e.g., "March 15, 2021")
        elif re.match(r"[A-Za-z]+ \d{1,2}, \d{4}", date_str):
            return datetime.strptime(date_str, "%B %d, %Y").strftime("%Y-%m-%d")
        # If only the year is found, default to January 1st
        elif re.match(r"\d{4}", date_str):
            return f"{date_str}-01-01"
    except ValueError:
        return None  # If parsing fails

    return None  # Default case


def infer_event_date_with_llm(query):
    """
    This function uses an LLM to infer the most probable date.
    """
    prompt = f"""
    Here is a query of an event for a company:
    {query}

    Please infer the most likely date this event happened. Return your response in strictly YYYY-MM-DD format.
    STILL PROVIDE THE DATE ONLY!!!

    DO NOT BE CONVERSATIONAL!!!! OUTPUT ONLY THE DATE!!!!!

    The output should be nothing but the format below:
    YYYY-MM-DD
    """

    llm_response = llm.invoke(prompt)
    print(llm_response)
    return normalize_date(llm_response.content.strip())


def parse_stock_data(stock_data):
    """
    Parses stock data to extract insights for each company.

    Args:
        stock_data (list): A list of dictionaries containing stock data for multiple companies.

    Returns:
        dict: A dictionary mapping company symbols to their summarized insights.
    """
    # Group data by company symbol
    company_data = defaultdict(list)
    for entry in stock_data:
        company_data[entry["symbol"]].append(entry)

    insights = {}

    for symbol, data in company_data.items():
        df = pd.DataFrame(data)

        # Ensure date is sorted in ascending order
        df.sort_values(by="date", inplace=True)

        # Calculate percentage change
        df["daily_return"] = df["close"].pct_change() * 100  # Percentage change
        df["volatility"] = df["high"] - df["low"]  # Intraday volatility
        df["moving_avg_7d"] = (
            df["close"].rolling(window=7).mean()
        )  # 7-day moving average

        # Identify largest single-day change
        max_drop = df.loc[df["daily_return"].idxmin()]
        max_gain = df.loc[df["daily_return"].idxmax()]

        # Identify trends
        start_price = df.iloc[0]["close"]
        end_price = df.iloc[-1]["close"]
        overall_change = ((end_price - start_price) / start_price) * 100

        # Volume trend (average and any major spikes)
        avg_volume = df["volume"].mean()
        high_volume_days = df[df["volume"] > (1.5 * avg_volume)]

        # Summary insights
        insights[symbol] = {
            "overall_price_change": round(overall_change, 2),
            "max_single_day_gain": {
                "date": str(max_gain["date"]),
                "percentage": round(max_gain["daily_return"], 2),
            },
            "max_single_day_drop": {
                "date": str(max_drop["date"]),
                "percentage": round(max_drop["daily_return"], 2),
            },
            "high_volume_days": [
                {"date": str(row["date"]), "volume": row["volume"]}
                for _, row in high_volume_days.iterrows()
            ],
            "7_day_moving_avg": df["moving_avg_7d"]
            .dropna()
            .tolist()[-5:],  # Last 5 entries for trend
        }

    return insights


# ---------------------------------------------------------------------------- #
#                     Example Usage for Starbucks Layoffs                      #
# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    company = "Starbucks"
    event = "Starbucks announces mass layoffs of around 15,000 people due to rising operational costs."
    ticker = "SBUX"

    analysis, details = analyze_company_highlight(company, event, ticker)
