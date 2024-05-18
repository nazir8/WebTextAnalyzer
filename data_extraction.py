import requests
from bs4 import BeautifulSoup

def extract_article_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        article_title = soup.find('title').text.strip()
        article_text = soup.get_text(separator='\n', strip=True)
        footer = soup.find('footer')
        if footer:
            footer.decompose()
        return article_title, article_text
    except Exception as e:
        print(f"Error extracting article from {url}: {e}")
        return None, None
