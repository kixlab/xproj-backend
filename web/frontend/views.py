from django.views.generic.base import TemplateView
from django.shortcuts import redirect

class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.year_of_birth is None:
            return redirect('accounts:onboarding')

        return super(IndexView, self).get(request, *args, **kwargs)
