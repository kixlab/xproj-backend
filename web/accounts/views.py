from django.views.generic.edit import UpdateView
from .forms import UserOnboardingForm, UserOnboarding2Form
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login, SuccessURLAllowedHostsMixin
from django.utils.http import is_safe_url


class OnboardingView(LoginRequiredMixin, SuccessURLAllowedHostsMixin, UpdateView):
    template_name = "account/onboarding.html"
    form_class = UserOnboardingForm
    form_step = 1
    form_total_steps = 2
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_object(self):
        return self.request.user

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        # verbatim copy from django.contrib.auth.views.LoginView
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

    def form_valid(self, form):
        self.object = form.save()
        next_step = self.form_step + 1
        url = reverse_lazy('accounts:onboarding_step_%d' % next_step)
        return redirect_to_login(self.get_redirect_url(), url)

    def get_context_data(self, **kwargs):
        context = super(OnboardingView, self).get_context_data(**kwargs)
        context.update({
            'redirect_field_name': self.redirect_field_name,
            'redirect_field_value': self.get_redirect_url(),
            'form_step': self.form_step,
            'form_total_steps': self.form_total_steps,
        })
        return context


class Onboarding2View(OnboardingView):
    template_name = "account/onboarding.html"
    form_class = UserOnboarding2Form
    form_step = 2


class Onboarding3View(OnboardingView):
    template_name = "account/onboarding_finish.html"
    form_class = UserOnboarding2Form
    form_step = 3