from django.conf.urls import url, include
from .views import PersonalizedPromptset

urlpatterns = [
    url(r'^api/prompt-sets/(?P<name>[^/.]+)/personalized/', PersonalizedPromptset.as_view(), name='promptset-personalized'),
]
