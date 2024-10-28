from django.urls import path
from .views import *

app_name = 'portfolio'

urlpatterns = [
    path('', index.as_view(), name = 'index'),
    path('callback', spotify_callback, name = 'callback'),
    path('get-last-commits', get_last_commits, name = 'get-last-commits'),
    path('get-current-song', current_song, name = 'get-current-song'),
    path('get-recently-played', recently_played, name = 'get-recently-played'),
]


