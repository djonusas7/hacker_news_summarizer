# Hacker News Article Summarizer

This is my first Boot.dev personal project. The point of this project is not to build a startup, ship a polished product, or make something resume-ready. The goal is to practice building something from scratch, breaking a project into smaller pieces, and getting more comfortable turning an idea into working code.

This project is also my first real attempt at working with Python, web scraping, and LLM models. It is intentionally a learning project, so the code is simple, direct, and focused on helping me understand the pieces involved.

## What It Does

The app is a terminal-based Hacker News article summarizer.

When you run it, the program:

1. Fetches the current top stories from Hacker News using the Hacker News API.
2. Looks through the top stories and collects the first five articles that have usable URLs.
3. Skips links from X/Twitter, since they are not good targets for article scraping.
4. Uses `WebBaseLoader` from LangChain to load the article text from each page.
5. Prompts the user for an OpenAI API key.
6. Uses an OpenAI chat model through LangChain to summarize each article.
7. Prints the article title, URL, and summary in the terminal.

The summaries include:

- Main idea
- Key takeaways
- Why it matters
- Reading time saved

Some articles may fail to load if the website blocks scrapers, requires JavaScript, or does not expose clean article text. When that happens, the app skips the summary for that article and prints a message explaining that the page could not be loaded.

## Why I Built It

This project was built for Boot.dev Personal Project 1.

The project requirements were to:

- Spend roughly 20-40 hours building something from scratch.
- Use a programming language I am already learning or familiar with.
- Commit code often and push it to GitHub.
- Create a README explaining what the project is and how to run it.
- Use third-party libraries when helpful, while still writing meaningful project code.

I chose this project because it gave me practice with several things at once:

- Making HTTP requests in Python.
- Reading JSON data from an API.
- Pulling article content from web pages.
- Working with environment variables and credentials.
- Using LangChain.
- Sending content to an LLM and formatting the response.
- Handling failures when pages cannot be scraped.

## Tech Used

- Python
- Requests
- PyYAML
- LangChain
- LangChain OpenAI
- LangChain Community `WebBaseLoader`
- OpenAI API
- Hacker News API

## How to Clone and Run

Clone the repository:

```bash
git clone <your-repository-url>
cd boot_dev_personal_project
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python main.py
```

When prompted, enter your OpenAI API key. You can create one from the OpenAI platform:

```text
https://platform.openai.com/account/api-keys
```

After the key is entered, the app will fetch the current top Hacker News articles, try to load their page content, and print summaries in the terminal.

## Notes About Credentials

The app asks for an OpenAI API key when it runs and saves it locally in `credentials.yml` for later use.

Do not commit `credentials.yml` to a public repository. API keys should be kept private.

## Current Limitations

- Some websites block scraping or require JavaScript, so not every article can be summarized.
- The app currently runs only in the terminal.
- The OpenAI API key flow is basic and meant for learning.

## Project Status

This is an early learning project and my first attempt at combining Python, scraping, and LLMs. The main goal was to build a working end-to-end program and learn from the process.
