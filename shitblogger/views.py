from django.shortcuts import render, redirect
from .models import BlogPost, Category
from django.views.generic import ListView, TemplateView
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Blog Index
class BlogIndex(TemplateView):
    
    template_name = 'shitblogger/blog-posts.html'
    context = {}

    def get(self, request):

        # Objects
        blog_posts = BlogPost.objects.filter(public = True).order_by('-created_at')

        # Paginator
        paginator_instance = Paginator(blog_posts, 20)
        page_number = request.GET.get('page')
        blogs_per_page = paginator_instance.get_page(page_number)

        # Context
        self.context['posts'] = blogs_per_page

        # Return
        return render(request, self.template_name, self.context)
    
    
    def post(self, request):

        print(request.POST)

        # POST - LOGIN
        if 'username' and 'password' in request.POST:
            # Authenticate user success
            if blog_login(request):
                messages.success(request, 'Login sucessful.')
                return render(request, self.template_name, self.context)

            # Authenticate user error
            messages.error(request, 'Invalid credentials.')
            return render(request, self.template_name, self.context)
        
        # POST - CREATE BLOG POST
        elif 'title' in request.POST:
            print(request.POST['title'])
            return render(request, self.template_name, self.context)

        

# Login function
def blog_login(request) -> bool:

    # Get user data
    username = request.POST['username']
    password = request.POST['password']

    # Authenticate
    user = authenticate(request, username=username, password=password)
    
    # Return result
    if user is not None:
        login(request, user)
        return True
    
    return False


# Logout function
def blog_logout(request):
    logout(request)
    return redirect('shitblogger:index')
 