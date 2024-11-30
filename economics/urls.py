from django.urls import path
from .views import *

app_name = 'economics'

urlpatterns = [
    path('home', index.as_view(), name = 'home'),
    path('fetch-all-indicators', fetch_all_values, name = 'fetch-all-indicators'),
    path('get-indicator/<str:indicator>', get_current_value, name = 'get-indicator'),
]
