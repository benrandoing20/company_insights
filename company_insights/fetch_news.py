from utils.news_api import fetch_news
from utils.tavily_api import fetch_tavily_results
from utils.file_manager import create_directory_structure, save_to_file
from utils.firecrawl_scraper import scrape_article


def scrape_news():
    companies = ["Starbucks"]

    for company in companies:
        print(f"Fetching news & search results for {company}...")

        # Create folder structure
        company_dir = create_directory_structure(company=company)

        # Fetch recent news articles
        news_articles = fetch_news(company, days=7, num_results=10)
        for idx, article in enumerate(news_articles):
            title = article.get("title", "No Title")
            url = article.get("url", "")

            # Scrape full article content using Firecrawl
            full_content = scrape_article(url) if url else "No URL available."

            # Save scraped content
            content = f"Title: {title}\nURL: {url}\n\n{full_content}"
            save_to_file(company_dir, f"news_{idx}.txt", content)

        # Fetch Tavily search results
        query = f"Tell me everything that happened with {company} in the past 7 days"
        search_results = fetch_tavily_results(query)

        # Save the full search result summary
        search_summary_content = f"Tavily Search Query: {query}\n\n"

        for idx, result in enumerate(search_results):
            title = result.get("title", f"search_{idx}")
            url = result.get("url", "")
            content = result.get(
                "content", "No content available"
            )  # Use extracted content if available
            score = result.get("score", "N/A")  # Confidence score of relevance

            # Append result to the summary file
            search_summary_content += f"Title: {title}\nURL: {url}\nRelevance Score: {score}\nSummary: {content[:500]}...\n\n"  # Truncate content

            # Save individual search result file
            search_result_content = f"Title: {title}\nURL: {url}\nRelevance Score: {score}\n\nFull Content:\n{content}"
            save_to_file(company_dir, f"search_{idx}.txt", search_result_content)

        # Save the overall search summary file
        save_to_file(company_dir, "tavily_search_summary.txt", search_summary_content)

        print(f"Data for {company} saved in {company_dir}")


if __name__ == "__main__":
    scrape_news()
