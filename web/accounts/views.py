from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth.views import LoginView
from .forms import UserOnboardingForm, UserOnboarding2Form
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login, SuccessURLAllowedHostsMixin
from django.utils.http import is_safe_url
from django.http import HttpResponse
from prompt_responses.views import CreateResponseView
from prompt_responses.models import Prompt
from django.db import transaction
from oauth2_provider.models import AccessToken
from django.utils.timezone import now

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
        context = super(Onboarding3View, self).get_context_data(**kwargs)
        context.update({
            'categories': categories_real
        })
        return context


class Onboarding4View(OnboardingViewMixin, TemplateView):
    "Finish"
    template_name = "account/onboarding_finish.html"
    form_class = UserOnboarding2Form
    form_step = 4


class ConsolidateUserView(LoginRequiredMixin, SuccessURLAllowedHostsMixin, RedirectView):
    """
    Merge the given user with the currently authenticated user.
    The other user is passed in by using a currently valid oauth token for that user.
    This sets all the models related to the other old user to the current new user.
    Redirects to the URL in the next query parameter
    """
    redirect_field_name = 'next'

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        # verbatim copy from LoginView
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

    def get(self, request):
        tok = self.request.GET.get('token', None)
        if not tok:
            return HttpResponse('Missing token', 400)
        try:
            token = AccessToken.objects.get(token=tok, expires__gte=now())
        except AccessToken.DoesNotExist:
            return HttpResponse('Invalid token', 400)

        old_user = token.user
        new_user = self.request.user
        if new_user.pk != old_user.pk:
            # Get all related fields and set to new user
            related_fields = [
                f for f in old_user._meta.get_fields()
                if (f.one_to_many or f.one_to_one)
                and not f.concrete
            ]
            for f in related_fields:
                # Update all related models
                # Note, this doesn't work for m2m at the moment
                f.related_model.objects.filter(**{f.remote_field.name: old_user}).update(**{f.remote_field.name: new_user})
        
        if not self.get_redirect_url():
            return HttpResponse('User has been migrated, but redirect URL is invalid.')
        return super().get(request)