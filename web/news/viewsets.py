from rest_framework import viewsets, filters
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from promises.serializers import *
from news.serializers import ArticleSerializer, ArticlePromisesSerializer
from news.models import Article
from promises.models import Promise


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    TODO this endpoint should be client_id verified since it creates objects. Probably also POST only
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)

    @list_route()
    def promises_for_url(self, request, pk=None):
        """
        Returns a list of promises related to the article found at a URL passed via query parameter
        """
        url = request.query_params.get('url', False)
        if not url:
            raise ValidationError({'error': 'url is required'})
        article = Article.get_or_create_by_url(url=url)
        article.analyze_article()
        context = {
            'request': request
        }
        serializer = ArticlePromisesSerializer(article, context=context)
        return Response(serializer.data)