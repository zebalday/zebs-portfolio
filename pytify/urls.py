from django.urls import path
from .views import *

app_name = 'pytify'

urlpatterns = [
    path('callback', spotify_callback, name = 'spotify-callback'),
]
