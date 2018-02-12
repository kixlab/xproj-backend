from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
import oauth2_provider.views
from oauth2_provider.models import Application
import uuid

class TokenView(oauth2_provider.views.TokenView):
    def create_token_response(self, request):
        post_data = request.POST.copy()
        email = post_data.pop('email', None)
        if email:
            username = get_user_model().objects.filter(email=email[0]).values_list('username', flat=True).last()
            post_data['username'] = username
            request.POST = post_data
        return super(TokenView, self).create_token_response(request)

class OAuthSuccessView(TemplateView):
    template_name = "oauth/success.html"

class AnnonymousSignupTokenView(oauth2_provider.views.TokenView):
    "Creates an anonymous user on the fly and returns an oauth token for authentication"
    def create_token_response(self, request):
        # Ensure the oauth app exists
        client_id = 'chromeextension-auto-signup'
        application, _ = Application.objects.get_or_create(
            client_id=client_id,
            defaults={
                'client_type': 'public',
                'authorization_grant_type': 'password',
                'name': 'Auto signup for browser extension',
                'skip_authorization': True
            })
        # Create new user
        User = get_user_model()
        username = uuid.uuid1()
        email = 'auto-%s@budgetwiser.org' % username
        password = User.objects.make_random_password()
        user = User(email=email, username=username)
        user.set_password(password)
        user.save()
        # Fake auth as this user
        post_data = {
            'username': username,
            'password': password,
            'client_id': client_id,
            'grant_type': 'password'
        }
        request.POST = post_data
        return super(AnnonymousSignupTokenView, self).create_token_response(request)


