from django.conf.urls import url
from .views import OnboardingView

urlpatterns = [
    url(r'^onboarding/', OnboardingView.as_view(), name='onboarding'),
]
