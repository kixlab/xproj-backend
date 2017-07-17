from django.conf.urls import url, include
from spatial import views

urlpatterns = [
    url(r'^reverse/', views.ReverseGeocodeView.as_view()),
]
