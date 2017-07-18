from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from allauth.account import views as allauth_views
from rest_framework.authtoken import views as rest_views

urlpatterns = []

# For local dev, serve static files directly from Django
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

# System views
urlpatterns += [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^login/', allauth_views.login, name="account_login"),
    url(r'^logout/', allauth_views.logout, name="account_logout"),
    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api/auth/signup/', include('rest_auth.registration.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# Apps
urlpatterns += [
    url(r'', include('spatial.urls')),
]
