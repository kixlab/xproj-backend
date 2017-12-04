from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^onboarding/$', OnboardingView.as_view(), name='onboarding'),
    url(r'^onboarding/location/', Onboarding2View.as_view(), name='onboarding_step_2'),
    url(r'^onboarding/interests/', Onboarding3View.as_view(), name='onboarding_step_3'),
    url(r'^onboarding/finish/', Onboarding4View.as_view(), name='onboarding_step_4'),
]
