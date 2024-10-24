from django.urls import path
from .views import *

app_name = 'portfolio'

urlpatterns = [
    path('', index.as_view(), name = 'index'),
    path('get-last-commits', get_last_commits, name = 'get-last-commits'),
]


