import urllib.request
from bs4 import BeautifulSoup

def load_article_soup(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
    
    return soup