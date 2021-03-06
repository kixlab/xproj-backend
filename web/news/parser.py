import urllib.request
from bs4 import BeautifulSoup
from django.utils.dateparse import parse_datetime
from pytz import timezone
import re
import logging
logger = logging.getLogger('xproject')

def load_article_soup(url):
    with urllib.request.urlopen(url, timeout=10) as response:
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
    return soup

def _get_publish_date_element(parser, doc):
    "Tries to find HTML element with publish date info"
    try:
        return parser.css_select(doc, '.sponsor .t11')[0]  # naver
    except IndexError:
        pass
    try:
        return parser.css_select(doc, '.info_view .txt_info')[0]  #daum
    except IndexError:
        pass
    return None

def parse_article_date(np_article):
    "Alternative date parsing, for when newspaper's parser fails"
    element = _get_publish_date_element(np_article.extractor.parser, np_article.clean_doc)
    if not element:
        return None
    date_string = parser.getText(element)
    if not date_string:
        return None
    date_string = re.sub(r'[^0-9:\-. ]+', '', date_string)
    date_string = date_string.strip().replace('. ', 'T').replace('.', '-').replace(' ', 'T') + ':00'
    dt = parse_datetime(date_string)
    if dt:
        return timezone('Asia/Seoul').localize(dt)
    return None

def load_article_naver(article):
    # Load article text when article is requested for the first time
    soup = load_article_soup(article.url)

    # Title
    article.title = soup.title.string
    
    # Date
    try:
        date_string = soup.select(".sponsor .t11")[0].string
        date_string = date_string.strip().replace(' ', 'T') + ':00'
        kst = timezone('Asia/Seoul')
        article.original_post_date = kst.localize(parse_datetime(date_string))
    except IndexError:
        pass

    # Text
    html = soup.find(id="articleBodyContents")
    for script in html("script"):
        script.decompose()
    for br in html.find_all("br"):
        br.replace_with("\n")
    article.text = str(html.get_text().strip())

def load_article_daum(article):
    # Load article text when article is requested for the first time
    soup = load_article_soup(article.url)

    # Title
    article.title = soup.title.string
    
    # Date
    try:
        date_string = soup.select(".info_view .txt_info")[1].string[3:] # timestamp starts from 3rd character
        date_string = date_string.strip().replace('.', '-').replace('- ', 'T') + ':00'
        kst = timezone('Asia/Seoul')
        article.original_post_date = kst.localize(parse_datetime(date_string))
    except IndexError:
        pass

    # Text
    # html = soup.find(id="articleBodyContents")
    html = soup.section
    for script in html("script"):
        script.decompose()
    for br in html.find_all("br"):
        br.replace_with("\n")
    article.text = str(html.get_text().strip())

