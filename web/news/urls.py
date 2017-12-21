from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^submit/$', ArticleSubmitView.as_view(), name='article_submit'),
]
