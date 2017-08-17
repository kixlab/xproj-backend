from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from spatial.viewsets import *
from promises.viewsets import *
from .router import Router

router = Router()
router.register(r'areas', AreaViewSet)
router.register(r'people', PersonViewSet)
router.register(r'voting-districts', VotingDistrictViewSet)
router.register(r'promises', PromiseViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api/auth/signup/', include('rest_auth.registration.urls')),
    url(r'^$', RedirectView.as_view(pattern_name='api_root', permanent=False)),
]