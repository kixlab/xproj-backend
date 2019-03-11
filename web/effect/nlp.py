import re
from konlpy.tag import Kkma, Hannanum, Twitter
import string
import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

kkma = Kkma()
hannanum = Hannanum()
twitter = Twitter()
remove_punct_map = dict.fromkeys(map(ord, string.punctuation))
remove_quotes_map = dict([(ord(x), " ") for x in ".․,‘’´“”·‧<>「」–-()~…"]) 

stopwords = "수 년 등 및 몇 중 네이버 뉴스".split()
stopwords += "공급 설치 조성 운영 실행 설립 확대 건설 제공 사업 실시 지원 검토 육성 추진 유치 강화 개선 구축 마련 확충 실시 개선 해소".split()
stopwords += ['것', '수', '있', '같', '좋', '되', '하', '더', '보', '없', '받', '대학', '생각', '대', '결국', '과', '블라인드', '필요']
stopwords = set(stopwords)

def tokenize(sent):
    return kkma.nouns(sent)

def get_top_n_words_from_tfidf_kor(corpus, n=10):
    vec = TfidfVectorizer(ngram_range=(1,2), stop_words = stopwords, max_features = 2000, analyzer = 'word', tokenizer = tokenize, max_df = 0.7).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()],
    words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]

def pos_tagger_for_model(text):
    "POS tags all parts of text and returns a list of 'Term/Tag' strings of specified tags"
    keep_tags = ('Noun', 'Verb', 'Adjective',)
    return ['/'.join(p) for p in twitter.pos(text, stem=True, norm=True) if p[0] not in stopwords and p[1] in keep_tags]

def clean_title(title):
    # Remove punctuation and quotes
    title = title.translate(remove_punct_map)
    title = title.translate(remove_quotes_map)
    # Collapse double spaces
    title = re.sub('\s+', ' ', title)
    return title

def filter_words(nouns):
    # Remove words with digits
    nouns = filter(lambda word: not any(char.isdigit() for char in word), nouns)
    # Remove blacklisted words
    badwords = ["수", "년", "등", "및", "몇", '네이버', '뉴스']
    badwords += ["공급", "설치", "조성", "운영", "설립", "확대", "건설", "제공"]
    nouns = filter(lambda word: word not in badwords, nouns)
    return list(nouns)

def title2nouns(title):
    "Turn a title into a list of all of its nouns, in the original order"
    return filter_words(hannanum.nouns(clean_title(title)))
    
def title2list(title):
    """Gather important nouns from a Korean text"""
    title = clean_title(title)
    titlewords = title.strip().split()

    nouns = []
    
    # Add special words
    if any(word != "대로" and word.endswith("대로") for word in titlewords):
        nouns.append("대로")
    if any(word != "도로" and word.endswith("도로") for word in titlewords):
        nouns.append("도로")

    # Gather relevant nouns from twitter and hannanum corpus
    for aword in titlewords:
        tlist = twitter.nouns(aword)
        hlist = hannanum.nouns(aword)
        htlist = list(set(hlist) - set(tlist))  # only in Hannanum
        thlist = list(set(tlist) - set(hlist))  # only in Twitter
        ilist = list(set(hlist) & set(tlist))   # in both
        
        # Add nouns that occur in both corpus
        nouns = nouns + ilist

        # Add all nouns from Twitter corpus that are long enough
        nouns = nouns + list(filter(lambda word: len(word) > 1, thlist))

        # Add nouns from Hannanum corpus that are non divisible (root noun)
        for htword in htlist:
            if len(htword) > 2:
                newlist = twitter.nouns(htword)
                if len(newlist) < 2:
                    nouns.append(htword)

    nouns = filter_words(nouns)
    return list(set(list(nouns)))

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

# Load training data
tagged = open('/data/nlp/train.json', 'r', encoding='utf-8')
tagkeys = json.load(tagged)
trainlist = [acat["keywords"] for acat in tagkeys]

def guess_category(text):
    "Guess a text's category by performing TFIDF"
    #nounList = kkma.nouns(text)
    nounList = text.translate(remove_punct_map).translate(remove_quotes_map).split()
    tfidf_mat = tfidf(nounList, trainlist)
    tfidf_score = np.dot(tfidf_mat, np.ones(shape=(len(nounList), 1)))
    catguess = int(np.argmax(tfidf_score))
    return [categories[catguess]]