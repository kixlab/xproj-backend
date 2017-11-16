from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from spatial.viewsets import *
from promises.viewsets import *
from news.viewsets import *
from .router import Router
from . import views
from prompt_responses.viewsets import PromptViewSet

router = Router()
router.register(r'areas', AreaViewSet)
router.register(r'people', PersonViewSet)
router.register(r'voting-districts', VotingDistrictViewSet)
router.register(r'promises', PromiseViewSet)
router.register(r'news', ArticleViewSet)
router.register(r'budget-programs', BudgetProgramViewSet)

# External packages
router.register(r'prompts', PromptViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api/auth/signup/', include('rest_auth.registration.urls')),
    url(r'^oauth/token/', views.TokenView.as_view()),
    url(r'^oauth/success/', views.OAuthSuccessView.as_view()),
    url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
#    url(r'^$', RedirectView.as_view(pattern_name='api_root', permanent=False)),
]
