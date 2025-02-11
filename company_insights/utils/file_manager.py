import os
from datetime import datetime


def create_directory_structure(base_dir="daily_data", company=""):
    """Creates a structured directory for storing results."""
    today = datetime.now().strftime("%Y-%m-%d")
    parent_dir = os.path.join(base_dir, today, company)
    os.makedirs(parent_dir, exist_ok=True)
    return parent_dir


def save_to_file(directory, filename, content):
    """Saves content to a text file in the specified directory."""
    file_path = os.path.join(directory, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
