# Company Insights: AI-Powered Portfolio Intelligence

An intelligent research assistant designed for hedge fund portfolio managers to explore how LLMs, agents, and automated tools can enhance investment decision-making. This project demonstrates a practical implementation of AI-driven market intelligence by automatically gathering news, analyzing events, and identifying historical parallels—all powered by local LLMs and modern AI tooling.

## Purpose

This project serves as a **hands-on exploration** for portfolio managers investigating how to leverage:
- **Large Language Models (LLMs)** for summarizing and analyzing market-moving news
- **AI Agents** for autonomous information gathering and pattern recognition
- **Automated Tools** (news APIs, web scraping, vector search) for continuous market monitoring

The system automatically runs every evening to:
1. Gather information from various news outlets about companies in your portfolio
2. Parse and summarize key market events using LLMs
3. Use AI agents to find historical analogues and analyze past stock behavior
4. Provide portfolio managers with actionable context for current market conditions

**Key Value Proposition**: Transform hours of manual research into automated, consistent intelligence gathering—allowing portfolio managers to focus on strategy rather than data collection.

---

## Table of Contents
1. [Purpose](#purpose)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Environment Configuration](#environment-configuration)
5. [Usage](#usage)
6. [Scheduling the Process](#scheduling-the-process)
7. [Contributing](#contributing)
8. [License](#license)

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

- **Query News Sources**: Use AI-powered tools (Tavily, News API, Firecrawl) to pull relevant market data
- **Summarize Events**: Leverage local LLMs (Llama 3.2 via Ollama) to parse and distill key information
- **Identify Historical Patterns**: Use AI agents to find analogous past events and analyze historical stock behavior
- **Generate Insights**: Provide portfolio managers with contextual intelligence for informed decision-making

This demonstrates how LLMs and agents can augment traditional research workflows with automated, scalable intelligence gathering.

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