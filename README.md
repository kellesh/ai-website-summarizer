# 🔎 AI Website Summarizer

A simple AI-powered tool that generates concise summaries from website URLs.

## Why?

Reading long articles, blogs, and documentation can be time-consuming. This tool helps you quickly understand the main points of a webpage using AI-generated summaries.

## Features

- Summarize website content from a URL
- AI-style summary output
- Query history sidebar
- One-click revisit of previous summaries
- Clean and lightweight Gradio UI

## Tech Stack

- Python
- Gradio
- BeautifulSoup / Requests
- AI Summarization Engine

## Installation

```bash
git clone https://github.com/<your-username>/ai-website-summarizer.git

cd ai-website-summarizer

python -m venv venv
source venv/bin/activate      # Linux/Mac

# OR

venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Open:

```text
http://localhost:7860
```

## How to Use

1. Enter a website URL.
2. Click **Summarize**.
3. Wait for processing to complete.
4. Review the generated summary.
5. Use the history panel to revisit previous queries.

## Project Structure

```text
.
├── app.py
├── summarizer.py
├── requirements.txt
└── README.md
```

## Future Enhancements

- Export summary to PDF
- Save history to database
- Search within summaries
- Multiple URL summarization

## License

MIT License

## Author

Built as a lightweight AI tool for faster web content consumption.


This version is concise, recruiter-friendly, and ideal for a GitHub project homepage.