from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.timezone import now
from promises.models import Promise
from urllib.parse import urlparse
from .parser import load_article_naver, load_article_daum
from promises.nlp import guess_category, title2list
from promises.matcher import promise_matcher
import logging
logger = logging.getLogger('xproject')

class Article(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    retrieved_date = models.DateTimeField(null=True, blank=True)
    original_post_date = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=254)
    title_keywords = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    url = models.CharField(max_length=254, unique=True)
    source = models.CharField(max_length=50)
    text = models.TextField(default="", blank=True)
    categories = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    promises = models.ManyToManyField(Promise, related_name='articles')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']

    def load_article(self):
        """Initial loading of article from source URL and parsing of document"""
        if self.retrieved_date is not None:
            return
        
        if self.source == 'news.naver.com':
            load_article_naver(self)
        elif self.source == 'v.media.daum.net':
            load_article_daum(self)
        else:
            # Unkown source
            self.text = "Unknown source"
            return

        if not self.text:
            self.text = "Text not found"

        self.retrieved_date = now()
        self.analyze_article()
        self.save()
    
    def analyze_article(self, redo=False):
        """Analyzing of loaded article"""
        if self.title and (not self.title_keywords or redo):
            self.title_keywords = title2list(self.title[:100])
        if self.text and (not self.categories or redo):
            self.categories = guess_category(self.text)
        if self.title and (not self.promises or redo):
            matches = promise_matcher.most_similar(self.title[:100])
            promise_ids = [match[2][1] for match in matches]
            self.promises = Promise.objects.filter(pk__in=promise_ids)

        """
        if self.categories:
            # Dummy
            self.promises = Promise.objects.filter(categories__overlap=self.categories,
                                                   person__mayor_for_province="서울특별시")[:10]
         """

    @classmethod
    def get_or_create_by_url(cls, url):
        parsed_uri = urlparse(url)
        
        article, created = cls.objects.get_or_create(url=url, defaults={
            'source': parsed_uri.netloc,
            'title': "Not loaded"
        })

        article.load_article()
    
        return article

