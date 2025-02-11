# Analogous Stock Evaluation

This project automatically runs every evening to gather information from various news outlets regarding desired companies, parses key summarized events, and then attempts to find past examples of similar happenings. This allows for quick and targeted knowledge of historical context and stock behavior around current events.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Environment Configuration](#environment-configuration)
4. [Usage](#usage)
5. [Scheduling the Process](#scheduling-the-process)
6. [Contributing](#contributing)
7. [License](#license)

---

## Prerequisites

1. **Git**  
    Make sure Git is installed to clone this repository.

    Check with: `git --version` in a terminal.

2. **[Ollama](https://github.com/jmorganca/ollama)**  
    Ollama is used to run the [Llama 3.2 model](https://github.com/jmorganca/ollama/blob/main/docs/models.md) locally.  
    *Installation instructions vary by system. Follow the link above to install Ollama

    Ensure you have downloaded and placed the llama3.2 model in the correct directory (commonly ~/.ollama). This is the default model so it should be installed upon installation.

## Installation

1. Clone the Repository

    `git clone https://github.com/your-username/your-repo.git`

    `cd your-repo`

2. Establish a Virtual Environment

    `uv venv venv`

    `source venv/bin/activate`

3. Using uv for Faster Installs, Install the Dependencies:

    `uv pip install .`

## Environment Configuration

1. Copy the Example Environment File

    `cp .env.example .env`

2. Open the newly created .env file and insert your keys:

    ```
    # Tavily Search
    TAVILY_API_KEY=<TAVILY_API_KEY>

    # News API
    NEWS_API_KEY=<NEWS_API_KEY>

    # Firecrawl API
    FIRECRAWL_API_KEY=<FIRECRAWL_API_KEY>
    ```

3. Source Your Environment File

    `source .env`

## Usage

After installing dependencies and configuring environment variables:

1. Activate the Virtual Environment (if not already active):

    `source venv/bin/activate`

2. Run the Script:

    `python company_insights/main.py`

The script will:

- Pull news data from configured sources
- Summarize key events
- Use Ollama (with the Llama 3.2 model) to draw parallels with past examples and evaluate the stock behavior of thos analagous examples.

## Scheduling the Process

This project is designed to run automatically every evening. You can configure it in several ways, for example using a cron job:

# Example crontab entry to run daily at 7 PM:
`0 19 * * * /path/to/venv/bin/python /path/to/your_project/your_script.py`

## Contributing

Contributions, suggestions, and improvements are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request.

## License

MIT License

Copyright (c) 2025 benrandoing20

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.