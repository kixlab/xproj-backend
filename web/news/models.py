from django.db import models
from django.contrib.postgres.fields import ArrayField
from promises.models import Promise
from urllib.parse import urlparse
from .parser import load_article_soup, analyze_article, title2list

class Article(models.Model):
    title = models.CharField(max_length=254)
    url = models.CharField(max_length=254, unique=True)
    source = models.CharField(max_length=50)
    text = models.TextField(default="", blank=True)
    categories = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    promises = models.ManyToManyField(Promise, related_name='articles')

    def __str__(self):
        return self.title

    def load_article(self):
        # Load article text when article is requested for the first time
        soup = load_article_soup(self.url)
        self.title = soup.title.string
        html = soup.find(id="articleBodyContents")
        for script in html("script"):
            script.decompose()
        for br in html.find_all("br"):
            br.replace_with("\n")
        self.text = str(html.get_text().strip())
        if not self.text:
            self.text = "Text not found"
            return
        analyze_article()
    
    def analyze_article(self):
        self.categories = analyze_article(self.text)
        self.promises = Promise.objects.filter(categories__overlap=self.categories,
                                               person__mop_for_district__areas__province="서울특별시")[:10]
    
    def save(self, *args, **kwargs):
        if not self.text:
            self.load_article()
        return super().save(*args, **kwargs)

    @classmethod
    def get_or_create_by_url(cls, url):
        parsed_uri = urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        
        article, created = cls.objects.get_or_create(url=url, defaults={
            'source': domain.rstrip('/'),
            'title': "Not loaded"
        })

        return article

