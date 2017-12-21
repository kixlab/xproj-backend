from django.contrib import admin
from django.db.models import Count
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_display = ('title', 'source', 'original_post_date', 'modified_date', 'categories', 'related_promises_count',)

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        return qs.annotate(promises_count=Count('promises'))

    def related_promises_count(self, inst):
        return inst.promises_count


admin.site.register(Article, ArticleAdmin)

