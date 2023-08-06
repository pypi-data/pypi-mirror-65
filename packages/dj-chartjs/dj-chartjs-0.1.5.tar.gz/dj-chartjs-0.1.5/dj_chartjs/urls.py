from django.urls import path
from django_charts.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
]