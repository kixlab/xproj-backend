import re
from konlpy.tag import Kkma, Hannanum, Twitter, Mecab
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from effect.models import Effect

kkma = Kkma()
hannanum = Hannanum()
twitter = Twitter()
mecab = Mecab()

remove_punct_map = dict.fromkeys(map(ord, string.punctuation))
remove_quotes_map = dict([(ord(x), " ") for x in ".․,‘’´“”·‧<>「」–-()~…"]) 

stopwords = "수 년 등 및 몇 중 네이버 뉴스".split()
stopwords += "공급 설치 조성 운영 실행 설립 확대 건설 제공 사업 실시 지원 검토 육성 추진 유치 강화 개선 구축 마련 확충 실시 개선 해소".split()
stopwords += ['것', '수', '있', '같', '좋', '되', '하', '더', '보', '없', '받', '대학', '생각', '대', '결국', '과', '블라인드', '필요', '거']
stopwords = set(stopwords)

words_freq_dict = {}

def tokenize(sent):
    return mecab.nouns(sent)

def get_keywords(queryset):
    corpus = list(queryset.values_list('description', flat=True))
    query = queryset.query
    keywords_all = get_top_n_words_from_tfidf_kor(corpus, query)
    keywords_all_txt = [k[0] for k in keywords_all]

    corpus_pos = list(queryset.filter(isBenefit = True).values_list('description', flat=True))
    query_pos = queryset.filter(isBenefit = True).query
    keywords_pos = get_top_n_words_from_tfidf_kor(corpus_pos, query_pos)
    keywords_pos_txt = [k[0] for k in keywords_pos]

    corpus_neg = list(queryset.filter(isBenefit = False).values_list('description', flat=True))
    query_neg = queryset.filter(isBenefit = False).query
    keywords_neg = get_top_n_words_from_tfidf_kor(corpus_neg, query_neg)
    keywords_neg_txt = [k[0] for k in keywords_neg]

    annotated = []

    for keyword in keywords_all:
        if keyword[0] in keywords_pos and keyword[0] in keywords_neg:
            annotated.append((keyword[0], keyword[1], 'both'))
        elif keyword[0] in keywords_pos:
            annotated.append((keyword[0], keyword[1], 'pos'))
        elif keyword[0] in keywords_neg:
            annotated.append((keyword[0], keyword[1], 'neg'))
        elif keyword[0] in keywords_pos:
            annotated.append((keyword[0], keyword[1], 'none'))

    return annotated



def get_top_n_words_from_tfidf_kor(corpus, query = None, n=10):
    words_freq = words_freq_dict.get(query)
    if words_freq is None:
        vec = CountVectorizer(ngram_range=(1,1), stop_words = stopwords, max_features = 1000, analyzer = 'word', tokenizer = tokenize, max_df = 0.7).fit(corpus)
        bag_of_words = vec.transform(corpus)
        sum_words = bag_of_words.sum(axis=0)
        words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
        words_freq.sort(key = lambda x: x[1], reverse = True)
        words_freq_dict[query] = words_freq[:10]
    #words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
        return words_freq[:n]
    else:
        return words_freq
