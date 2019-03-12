import re
from konlpy.tag import Kkma, Hannanum, Twitter
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

kkma = Kkma()
hannanum = Hannanum()
twitter = Twitter()
#mecab = Mecab()

remove_punct_map = dict.fromkeys(map(ord, string.punctuation))
remove_quotes_map = dict([(ord(x), " ") for x in ".․,‘’´“”·‧<>「」–-()~…"]) 

stopwords = "수 년 등 및 몇 중 네이버 뉴스".split()
stopwords += "공급 설치 조성 운영 실행 설립 확대 건설 제공 사업 실시 지원 검토 육성 추진 유치 강화 개선 구축 마련 확충 실시 개선 해소".split()
stopwords += ['것', '수', '있', '같', '좋', '되', '하', '더', '보', '없', '받', '대학', '생각', '대', '결국', '과', '블라인드', '필요', '거']
stopwords = set(stopwords)

words_freq_dict = {}

def tokenize(sent):
    return hannanum.nouns(sent)

def get_top_n_words_from_tfidf_kor(corpus, query = None, n=10):
    words_freq = words_freq_dict.get(query)
    if words_freq is None:
        vec = TfidfVectorizer(ngram_range=(1,2), stop_words = stopwords, max_features = 500, analyzer = 'word', tokenizer = tokenize, max_df = 0.7).fit(corpus)
        bag_of_words = vec.transform(corpus)
        sum_words = bag_of_words.sum(axis=0)
        words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
        words_freq.sort(key = lambda x: x[1], reverse = True)
        words_freq_dict[query] = words_freq[:10]
    #words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
        return words_freq[:n]
    else:
        return words_freq
