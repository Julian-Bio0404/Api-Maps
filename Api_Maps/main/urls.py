"""Main URLs."""

# Django
from django.urls import path

# Views
from . import views

app_name = 'main'
urlpatterns = [
    path('route', views.route, name='route'),
    path('map', views.map, name='map')
]