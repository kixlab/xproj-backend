from django.conf.urls import url, include
from rest_framework import routers
from spatial import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'areas', views.AreaViewSet)
router.register(r'person', views.PersonViewSet)
router.register(r'voting-districts', views.VotingDistrictViewSet)
router.register(r'promises', views.PromiseViewSet)
router.register(r'reverse-geocode', views.ReverseGeocodeAPIView, base_name='Area')

urlpatterns = [
    url(r'^spatial/reverse/', views.ReverseGeocodeView.as_view()),
    url(r'^api/', include(router.urls))
]