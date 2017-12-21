from django import forms
from .models import Article

class ArticleSubmitForm(forms.Form):
    url = forms.CharField()

    def submit_article(self):
        url = self.cleaned_data['url']
        article = Article.get_or_create_by_url(url=url)
        return article