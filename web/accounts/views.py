from django.views.generic.edit import UpdateView
from .forms import UserOnboardingForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model


class OnboardingView(LoginRequiredMixin, UpdateView):
    template_name = "account/onboarding.html"
    form_class = UserOnboardingForm
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

