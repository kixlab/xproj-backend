from django.views.generic.edit import FormView
from .forms import ArticleSubmitForm
from promises.matcher import promise_matcher
from promises.models import Promise

class ArticleSubmitView(FormView):
    template_name = 'news/article_submit.html'
    form_class = ArticleSubmitForm
    success_url = '/thanks/'

    def form_valid(self, form):
        article = form.submit_article()
        context = self.get_context_data(form=form)
        context['article'] = article

        matches = promise_matcher.most_similar(article.title[:100], n=10, threshold=0.1)
        promises = [{'score': '%d' % (100*match[1]), 'object': Promise.objects.get(pk=match[2][1])} for match in matches]
        context['promises'] = promises

        return self.render_to_response(context)