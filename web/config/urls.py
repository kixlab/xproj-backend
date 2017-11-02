from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from allauth.account import views as allauth_views
from rest_framework.authtoken import views as rest_views
from frontend.views import IndexView

urlpatterns = []

# System views
urlpatterns += [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^login/', allauth_views.login, name="account_login"),
    url(r'^logout/', allauth_views.logout, name="account_logout"),
]

# Apps
urlpatterns += [
    url(r'', include('api.urls')),
    url(r'^$', IndexView.as_view(), name='home')
]

# For local dev, serve static files directly from Django
# In deployment, these should be served from a real server
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns