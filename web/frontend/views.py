from django.views.generic.base import TemplateView
from django.shortcuts import redirect

class IndexView(TemplateView):
    template_name = "index.html"
