# job_scraper.py
import requests
from bs4 import BeautifulSoup

def extract_job_description(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # This is naive – can be improved per site
    job_description = soup.get_text(separator="\n")
    return job_description.strip()
