from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from allauth.account import views as allauth_views

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
]

# Apps
urlpatterns += [
    url(r'^spatial/', include('spatial.urls')),
]
