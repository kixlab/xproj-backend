from django.views.generic.edit import UpdateView
from .forms import UserOnboardingForm, UserOnboarding2Form
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model


class OnboardingView(LoginRequiredMixin, UpdateView):
    template_name = "account/onboarding.html"
    form_class = UserOnboardingForm
    form_step = 1
    form_total_steps = 2

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        next_step = self.form_step + 1
        url = reverse_lazy('accounts:onboarding_step_%d' % next_step)
        return url

    def get_context_data(self, **kwargs):
        context = super(OnboardingView, self).get_context_data(**kwargs)
        context['form_step'] = self.form_step
        context['form_total_steps'] = self.form_total_steps
        return context


class Onboarding2View(OnboardingView):
    template_name = "account/onboarding.html"
    form_class = UserOnboarding2Form
    form_step = 2


class Onboarding3View(OnboardingView):
    template_name = "account/onboarding_finish.html"
    form_class = UserOnboarding2Form
    form_step = 3