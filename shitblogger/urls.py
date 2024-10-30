from django.urls import path
from .views import *

app_name = 'shitblogger'

urlpatterns = [
    path('', BlogIndex.as_view(), name = 'index'),
    path('logout', blog_logout, name = 'logout'),
    path('add-cat', add_category, name = 'add-category'),
    path('add-post', add_blog_post, name = 'add-blog-post'),
]
