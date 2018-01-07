from promises.models import Promise
from promises.nlp import title2nouns, stopwords, pos_tagger_for_model

from gensim.models.doc2vec import TaggedDocument
from django.core.exceptions import ObjectDoesNotExist
from gensim import corpora, models, similarities
import logging
from itertools import tee

logger = logging.getLogger('xproject')

class QuerysetDocIterator(object):
    """
    Iterator that turns a queryset into documents suitable for gensim.
    transform should be a callable than turns a model object into a tuple of (text, labels)
    """
    def __init__(self, queryset, transform=None):
        self.queryset = queryset
        if not transform:
            self.transform = lambda obj: (str(obj), [obj.pk])
        else:
            self.transform = transform

    def __iter__(self):
        "Iterator over queryset, retrieves data in chunks"
        chunk_size = 500
        queryset = self.queryset
        try:
            last_pk = queryset.order_by('-pk')[:1].get()['pk']
        except ObjectDoesNotExist:
            return
        
        pk = 0
        queryset = queryset.order_by('pk')
        idx = -1
        while pk < last_pk:
            for row in queryset.filter(pk__gt=pk)[:chunk_size]:
                idx += 1
                pk = row['pk']
                doc = self.transform(row)
                yield TaggedDocument(words=doc[0], tags=[idx, pk])


class DocumentMatcher(object):
    lsi = None

    def __init__(self, queryset, document_transform=None):
        self.queryset = queryset
        self.document_transform = document_transform

    def get_queryset(self):
        return self.queryset

    def get_document_iterator(self, queryset):
        return QuerysetDocIterator(queryset, transform=self.document_transform)

    def build_model(self):
        logger.debug('Matcher - Retrieving documents...')
        queryset = self.get_queryset()
        documents = list(self.get_document_iterator(queryset))
        
        dictionary_ko = corpora.Dictionary.load('/data/ko.dict')

        num_topics = 40

        logger.debug('Matcher - Building Lsi model...')
        # Generate Lsi model for promise text corpus
        corpus = [dictionary_ko.doc2bow(text.words) for text in documents]
        # Train Lsi model
        self.lsi = models.LsiModel(corpus, id2word=dictionary_ko, num_topics=num_topics)
        # Transform corpus to LSI space and index it
        self.index = similarities.MatrixSimilarity(self.lsi[corpus])
        
        self.dictionary_ko = dictionary_ko
        self.documents = documents

    def most_similar(self, text, n=99, threshold=0.6):
        """
        Gets the n documents most similar to the text.
        This analyzes the text for nouns, so please use short texts (like titles) only.
        Returns list of (promise_id, score) tuples
        """
        if not self.lsi:
            self.build_model()

        tagged_text = pos_tagger_for_model(text)

        logger.debug('Matcher - Searching for documents similar to %s (%s)' % (text, ' '.join(tagged_text)))

        # Convert text to bag of words
        vec_bow = self.dictionary_ko.doc2bow(tagged_text)
        # Convert the query to LSI space
        vec_lsi = self.lsi[vec_bow]
        # Perform a similarity query against the corpus
        sims = [item + (self.documents[item[0]].tags,) for item in enumerate(self.index[vec_lsi])]
        if threshold:
            sims = filter(lambda item: item[1] >= threshold, sims)
        # Return the similarities sorted by descending score
        if not sims:
            logger.debug('Matcher - No matches for %s (n=%d, threshold=%.2f)' % (text, n, threshold))
            return []
        sims = sorted(sims, key=lambda item: -item[1])
        logger.debug('Matcher - %d matches for %s (n=%d, threshold=%.2f)' % (len(sims), text, n, threshold))
        return sims[:n]

class PromiseMatcher(DocumentMatcher):
    def __init__(self):
        self.document_transform = lambda p: (pos_tagger_for_model(p['title']), [p['pk']], )
    
    def get_queryset(self):
        return Promise.objects.filter(person__mayor_for_province="서울특별시").values('pk', 'title')
        #return Promise.objects.filter(person__mayor_for_province="서울특별시").values('pk', 'title')

# Global instance of promise matcher
promise_matcher = PromiseMatcher()
