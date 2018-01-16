from django.urls import reverse
from django.contrib.auth.views import redirect_to_login
from django.contrib.staticfiles.views import serve as serve_static


class ForceOnboardingMiddleware:
    """
    This middleware redirects the user to the onboarding views if they haven't
    provided the personal information yet
    """

    def _is_normal_request(self, request):
        if not request.resolver_match:
            return False
        if request.resolver_match.func == serve_static or not request.path:
            return False
        if 'onboarding' in request.path or 'api' in request.path or 'confirm-email' in request.path or 'logout' in request.path:
            return False
        return True

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated and request.user.year_of_birth is None:
            if self._is_normal_request(request):
                return redirect_to_login(request.get_full_path(), reverse('accounts:onboarding'))