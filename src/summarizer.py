import openai
import dotenv
from scraper import fetch_website_contents
import os
dotenv.load_dotenv()          # <-- this reads your .env file
client = openai.OpenAI(api_key = os.getenv("API_KEY") , base_url=os.getenv("BASE_URL"))

system_prompt = """You analyze the contents of a website and
give a short, friendly summary. Ignore navigation menus.
Respond in markdown."""

def summarize(url):
    website = fetch_website_contents(url)
    response = client.chat.completions.create(
        model= os.getenv("MODEL"),
        messages=[
            {"role":"system", "content": system_prompt},
            {"role":"user",   "content": f"Summarize this website:\n\n{website}"},
        ],
    )
    return response.choices[0].message.content