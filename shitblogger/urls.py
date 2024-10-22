from django.urls import path
from .views import *

app_name = 'shitblogger'

urlpatterns = [
    path('shitposts', BlogIndex.as_view(), name = 'index'),
    path('logout', blog_logout, name = 'logout')
]
