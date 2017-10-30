import urllib.request
from bs4 import BeautifulSoup
import json
import sys
import numpy as np
from konlpy.tag import Kkma, Hannanum, Twitter
from konlpy.utils import pprint
import string
from django.utils.dateparse import parse_datetime
from pytz import timezone

def load_article_soup(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
    
    return soup

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

kkma = Kkma()
hannanum = Hannanum()
twitter = Twitter()
remove_punct_map = dict.fromkeys(map(ord, string.punctuation))
remove_quotes_map = dict([(ord(x), None) for x in "‘’´“”–-"]) 

def tfidf(ttlist, trainlist):
    tlen = len(ttlist)
    clen = len(trainlist)
    tfidf_mat = np.zeros(shape=(clen,tlen))
    tf_mat = tfidf_mat
    idf_mat = np.zeros(tlen)
    for t in range(tlen):
        term = ttlist[t]
        dfcount = 0
        for c in range(clen):
            cdoc = trainlist[c]
            tf_mat[c,t] = cdoc.count(term)
            if term in cdoc:
                dfcount = dfcount+1
        idf_mat[t] = dfcount/clen
    tfidf_mat = np.dot(tf_mat, np.diag(idf_mat))
    return tfidf_mat

def title2list(title):
    # Remove punctuation
    title = title.replace("…", " ")
    title = title.translate(remove_punct_map)
    title = title.translate(remove_quotes_map)
    titlewords = title.strip().split()

    entities = []
    
    # Add special words
    if any(word != "대로" and word.endswith("대로") for word in titlewords):
        entities.append("대로")
    if any(word != "도로" and word.endswith("도로") for word in titlewords):
        entities.append("도로")

    # Gather relevant words from twitter and hannanum corpus
    for aword in titlewords:
        awordlist = []
        tlist = twitter.nouns(aword)
        hlist = hannanum.nouns(aword)
        htlist = list(set(hlist) - set(tlist))
        thlist = list(set(tlist) - set(hlist))
        ilist = list(set(hlist) & set(tlist))
        awordlist = ilist
        if len(htlist)>0:
            for htword in htlist:
                newlist = twitter.nouns(htword)
                if len(newlist) < 2:
                    awordlist.append(htword)
        if len(thlist) > 0:
            for thword in thlist:
                if len(thword) > 1:
                    awordlist.append(thword)
        
        entities = entities + awordlist
    
    # Remove words with digits
    entities = filter(lambda word: not any(char.isdigit() for char in word), entities)
    # Blacklist
    badwords = ["수", "년", "등", "몇", '네이버', '뉴스']
    entities = filter(lambda word: word not in badwords, entities)
    return list(set(list(entities)))

# Load training data
tagged = open('/data/nlp/train.json', 'r', encoding='utf-8')
tagkeys = json.load(tagged)
categories = ['안전/환경', '일자리', '문화체육', '보건복지', '교통/건설', '정치행정', '경제', '과학기술', '외교안보', '교육', '농축수산', '인권', '기타']

trainlist = []
for acat in tagkeys:
    catwords = acat["keywords"]
    trainlist.append(catwords)

def guess_category(text):
    #nounList = kkma.nouns(text)
    nounList = text.translate(remove_punct_map).translate(remove_quotes_map).split()
    tfidf_mat = tfidf(nounList, trainlist)
    tfidf_score = np.dot(tfidf_mat, np.ones(shape=(len(nounList), 1)))
    catguess = int(np.argmax(tfidf_score))
    return [categories[catguess]]
