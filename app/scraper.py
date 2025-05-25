import requests
from bs4 import BeautifulSoup

def scrape_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        for script in soup(["script", "style", "nav", "header", "footer"]):
            script.extract()
        text = soup.get_text(separator="\n")
        lines = [line.strip() for line in text.splitlines()]
        clean_text = "\n".join([line for line in lines if line])
        return clean_text
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None
