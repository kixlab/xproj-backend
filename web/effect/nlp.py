import re
from konlpy.tag import Mecab
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from effect.models import Effect

# kkma = Kkma()
# hannanum = Hannanum()
# twitter = Twitter()
mecab = Mecab()

remove_punct_map = dict.fromkeys(map(ord, string.punctuation))
remove_quotes_map = dict([(ord(x), " ") for x in ".․,‘’´“”·‧<>「」–-()~…"]) 

stopwords = []
# stopwords = "수 년 등 및 몇 중 네이버 뉴스".split()
# stopwords += "공급 설치 조성 운영 실행 설립 확대 건설 제공 사업 실시 지원 검토 육성 추진 유치 강화 개선 구축 마련 확충 실시 개선 해소".split()
stopwords += ['것', '수', '있', '같', '좋', '되', '하', '더', '보', '없', '받', '이', '생각', '대', '내', '결국', '과', '블라인드', '필요', '거', '때문', '때', '데', '경우', '취', '준', '나', '저', '부분', '관', '혼', '런', '지']
stopwords = set(stopwords)

words_freq_dict = {}
vectorizer = [None, None]
words_freqs = [None, None]
def tokenize(sent):
    return mecab.nouns(sent)

def get_keywords(queryset, policy, isPos): #TODO: Optimize more by storing keywords
    # Fetch keywords list
    corpus = list(queryset.values_list('description', flat=True))
    keywords_all = get_top_n_words_from_tfidf_kor(corpus, policy)

    corpus_pos = list(queryset.filter(isBenefit = 1).values_list('description', flat=True))
    keywords_pos = get_top_n_words_from_tfidf_kor(corpus_pos, policy)
    keywords_pos_txt = [k[0] for k in keywords_pos]

    corpus_neg = list(queryset.filter(isBenefit = 0).values_list('description', flat=True))
    keywords_neg = get_top_n_words_from_tfidf_kor(corpus_neg, policy)
    keywords_neg_txt = [k[0] for k in keywords_neg]
    
    annotated = []

    if isPos is None:
        for keyword in keywords_all:
            if keyword[0] in keywords_pos_txt and keyword[0] in keywords_neg_txt:
                annotated.append((keyword[0], keyword[1], 'both'))
            elif keyword[0] in keywords_pos_txt:
                annotated.append((keyword[0], keyword[1], 'pos'))
            elif keyword[0] in keywords_neg_txt:
                annotated.append((keyword[0], keyword[1], 'neg'))
            else:
                annotated.append((keyword[0], keyword[1], 'none'))
    elif isPos == '1':
        for keyword in keywords_pos:
            if keyword[0] in keywords_neg_txt:
                annotated.append((keyword[0], keyword[1], 'both'))
            else:
                annotated.append((keyword[0], keyword[1], 'pos'))
    elif isPos == '0':
        for keyword in keywords_neg:
            if keyword[0] in keywords_pos_txt:
                annotated.append((keyword[0], keyword[1], 'both'))
            else:
                annotated.append((keyword[0], keyword[1], 'neg'))
    elif isPos == 'all':
        annotated = [[], [], []]
        for keyword in keywords_neg:
            if keyword[0] in keywords_pos_txt:
                annotated[2].append((keyword[0], keyword[1], 'both'))
            else:
                annotated[2].append((keyword[0], keyword[1], 'neg'))
        for keyword in keywords_pos:
            if keyword[0] in keywords_neg_txt:
                annotated[1].append((keyword[0], keyword[1], 'both'))
            else:
                annotated[1].append((keyword[0], keyword[1], 'pos'))
        for keyword in keywords_all:
            if keyword[0] in keywords_pos_txt and keyword[0] in keywords_neg_txt:
                annotated[0].append((keyword[0], keyword[1], 'both'))
            elif keyword[0] in keywords_pos_txt:
                annotated[0].append((keyword[0], keyword[1], 'pos'))
            elif keyword[0] in keywords_neg_txt:
                annotated[0].append((keyword[0], keyword[1], 'neg'))
            else:
                annotated[0].append((keyword[0], keyword[1], 'none'))

    return annotated


# def get_top_n_words_from_tfidf_kor(corpus, query = None, n=10):
#     if len(corpus) < 10:
#         return []
#     words_freq = words_freq_dict.get(query)
#     if words_freq is None:
#         vec = CountVectorizer(ngram_range=(1,1), stop_words = stopwords, max_features = 1000, analyzer = 'word', tokenizer = tokenize, max_df = 0.8).fit(corpus)
#         bag_of_words = vec.transform(corpus)
#         sum_words = bag_of_words.sum(axis=0)
#         words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
#         words_freq.sort(key = lambda x: x[1], reverse = True)
#         words_freq_dict[query] = words_freq[:10]
#     #words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
#         return words_freq[:n]
#     else:
#         return words_freq

# def get_top_n_words_from_tfidf_kor(corpus, policy, n = 30): Sum of TF-IDF score version
#     if len(corpus) is 0:
#         return []
    
#     if vectorizer[policy - 1] is None:
#         totalCorpus = list(Effect.objects.filter(is_guess = False).values_list('description', flat=True))
#         vectorizer[policy - 1] = CountVectorizer(ngram_range=(1, 1), stop_words = stopwords, max_features = 1000, analyzer = 'word', tokenizer = tokenize).fit(totalCorpus)
    
#     bag_of_words = vectorizer[policy - 1].transform(corpus)
#     sum_words = bag_of_words.sum(axis=0)
#     words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer[policy - 1].vocabulary_.items()]
#     words_freq.sort(key = lambda x: x[1], reverse = True)
#     return words_freq[:n]

def get_top_n_words_from_tfidf_kor(corpus, policy, n = 30):
    if len(corpus) < 10:
        return []
    
    if vectorizer[policy - 1] is None:
        totalCorpus = list(Effect.objects.filter(is_guess = False).values_list('description', flat=True))
        vectorizer[policy - 1] = CountVectorizer(ngram_range=(1,1), stop_words = stopwords, max_features = 1000, analyzer = 'word', tokenizer = tokenize, min_df=5, max_df=0.8).fit(totalCorpus)
        bow = vectorizer[policy - 1].transform(totalCorpus)
        sw = bow.sum(axis=0)
        wf = [(word, sw[0, idx]) for word, idx in vectorizer[policy - 1].vocabulary_.items()]
        words_freqs[policy - 1] = wf
        
    bag_of_words = vectorizer[policy - 1].transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer[policy - 1].vocabulary_.items()]

    words_freq_ratio = [(i[0], i[1]/j[1]) for i, j in zip(words_freq, words_freqs[policy - 1])]
    words_freq_ratio.sort(key = lambda x: x[1], reverse = True)
    return words_freq_ratio[:n]