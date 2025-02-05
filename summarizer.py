import os
import glob
import ollama
from datetime import datetime
from utils.file_manager import create_directory_structure, save_to_file


def load_text_files(directory):
    """Loads all text files from a given directory and combines them into a list."""
    file_paths = glob.glob(os.path.join(directory, "*.txt"))
    articles = []
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as f:
            articles.append(f.read())
    return articles


def extract_key_insights(articles):
    """Summarizes key points and extracts subtle insights using an LLM (Ollama)."""
    combined_text = "\n\n".join(articles)  # Combine articles for LLM processing

    prompt = f"""
    Extract the essential one-liners summarizing key events in the business news. 
    Then, analyze the overall sentiment, financial tone, and any unique insights that a human might not recognize immediately.

    Here is the news data:
    {combined_text}

    Provide:
    1. Essential one-liners for what happened.
    2. Sentiment analysis (positive/negative/neutral).
    3. Any unique or hidden insights.
    """

    response = ollama.chat(
        model="llama3.2", messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"].strip()


def summarize_news():
    """Main function to aggregate and summarize the daily news insights."""
    today = datetime.now().strftime("%Y-%m-%d")
    base_dir = f"./daily_data/{today}"

    companies = os.listdir(base_dir)  # Get company folders
    summary_dir = create_directory_structure(base_dir=base_dir, company="summaries")

    for company in companies:
        company_dir = os.path.join(base_dir, company)
        if not os.path.isdir(company_dir):
            continue  # Skip if not a directory

        articles = load_text_files(company_dir)
        if not articles:
            continue

        summary = extract_key_insights(articles)
        save_to_file(summary_dir, f"{company}_summary.txt", summary)

        print(f"Summary saved for {company}")


if __name__ == "__main__":
    summarize_news()
