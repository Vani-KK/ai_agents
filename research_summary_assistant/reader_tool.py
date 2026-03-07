import requests
from bs4 import BeautifulSoup

def read_article(url):
    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print("Failed to fetch page")
            return ""

        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")

        text = " ".join([p.get_text() for p in paragraphs])

        print("Extracted characters:", len(text))

        if len(text) < 200:
            print("Warning: very little text extracted")

        return text[:4000]

    except Exception as e:
        print("Reader error:", e)
        return ""