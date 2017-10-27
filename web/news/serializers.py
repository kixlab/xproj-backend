from rest_framework import serializers
from news.models import Article
from promises.serializers import PromiseSerializer
from rest_framework.utils.field_mapping import get_url_kwargs


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(**get_url_kwargs(Article))
    original_url = serializers.CharField(source='url')
    
    class Meta:
        model = Article
        fields = ('url', 'original_url', 'source', 'title', 'categories', )

class ArticlePromisesSerializer(ArticleSerializer):
    promises = PromiseSerializer(many=True) 

    class Meta:
        model = Article
        fields = ('url', 'original_url', 'source', 'title', 'categories', 'promises', 'text',)