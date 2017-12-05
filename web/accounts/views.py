from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from .forms import UserOnboardingForm, UserOnboarding2Form
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login, SuccessURLAllowedHostsMixin
from django.utils.http import is_safe_url
from prompt_responses.views import CreateResponseView
from prompt_responses.models import Prompt
from django.db import transaction

from news import categories_real


class OnboardingViewMixin(LoginRequiredMixin, SuccessURLAllowedHostsMixin):
    form_step = 1
    form_total_steps = 3
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_context_data(self, **kwargs):
        context = super(OnboardingViewMixin, self).get_context_data(**kwargs)
        context.update({
            'redirect_field_name': self.redirect_field_name,
            'redirect_field_value': self.get_redirect_url(),
            'form_step': self.form_step,
            'form_total_steps': self.form_total_steps,
            'steps': range(1, self.form_total_steps+2)
        })
        return context

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        next_step = self.form_step + 1
        url = reverse_lazy('accounts:onboarding_step_%d' % next_step)
        return redirect_to_login(self.get_redirect_url(), url)

# Copy method from LoginView
OnboardingViewMixin.get_redirect_url = LoginView.get_redirect_url

class OnboardingView(OnboardingViewMixin, UpdateView):
    "User demorgaphic information"
    template_name = "account/onboarding.html"
    form_class = UserOnboardingForm

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class Onboarding2View(OnboardingViewMixin, UpdateView):
    "User location"
    template_name = "account/onboarding_location.html"
    form_class = UserOnboarding2Form
    form_step = 2

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class Onboarding3View(OnboardingViewMixin, CreateResponseView):
    "User interests, saved as a Response with prompt_responses framework"
    template_name = "account/onboarding_interests.html"
    form_step = 3

    def get_prompt(self):
        settings = {
            'type': 'openended',
            'text': 'User interests at onboarding',
            'prompt_object_type': None,
            'response_object_type': None,
        }
        prompt, _ = Prompt.objects.update_or_create(name='user-interests', defaults=settings)
        return prompt

    def form_valid(self, form):
        form.instance.user = self.get_user()
        self.object = form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OnboardingViewMixin, self).get_context_data(**kwargs)
        context.update({
            'categories': categories_real
        })
        return context


class Onboarding4View(OnboardingViewMixin, TemplateView):
    "Finish"
    template_name = "account/onboarding_finish.html"
    form_class = UserOnboarding2Form
    form_step = 4