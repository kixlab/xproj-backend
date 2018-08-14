from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from spatial.viewsets import *
from promises.viewsets import *
from news.viewsets import *
from .router import Router
from . import views
from prompt_responses.viewsets import PromptViewSet, PromptSetViewSet
from rest_auth.registration.views import RegisterView, VerifyEmailView
from policy.viewsets import *
from effect.viewsets import *
from stakeholdergroup.viewsets import *
from empathy.viewsets import *
from novelty.viewsets import *
from userpolicy.viewsets import *
from minisurvey.viewsets import *
from userprofile.viewsets import *
router = Router()
router.register(r'areas', AreaViewSet)
router.register(r'people', PersonViewSet)
router.register(r'voting-districts', VotingDistrictViewSet)
router.register(r'promises', PromiseViewSet)
router.register(r'news', ArticleViewSet)
router.register(r'budget-programs', BudgetProgramViewSet)
router.register(r'policies', PolicyViewSet)
router.register(r'effects', EffectViewSet)
router.register(r'stakeholdergroups', StakeholderGroupViewSet)
router.register(r'empathy', EmpathyViewSet)
router.register(r'novelty', NoveltyViewSet)
router.register(r'userpolicy', UserPolicyViewSet)
router.register(r'minisurvey', MiniSurveyViewSet)
router.register(r'userprofile', UserProfileViewSet)
# External packages
router.register(r'prompts', PromptViewSet)
router.register(r'prompt-sets', PromptSetViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/auth/', include('rest_auth.urls')),

    url(r'^api/auth/signup/$', RegisterView.as_view(), name='rest_register'),
    url(r'^api/auth/signup/verify-email/$', VerifyEmailView.as_view(), name='rest_verify_email'),

    url(r'^oauth/token/', views.TokenView.as_view()),
    url(r'^oauth/success/', views.OAuthSuccessView.as_view()),
    url(r'^oauth/auto-signup/', views.AnnonymousSignupTokenView.as_view()),
    url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
#    url(r'^$', RedirectView.as_view(pattern_name='api_root', permanent=False)),
]
