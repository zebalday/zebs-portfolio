from django.shortcuts import render, redirect
from .models import BlogPost, Category
from .forms import BlogForm, CategoryForm
from .serializers import BlogPostSerializer
from django.views.generic import ListView, TemplateView
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Blog Index
class BlogIndex(TemplateView):
    
    template_name = 'shitblogger/blog-posts.html'
    context = {}

    def get(self, request):

        # Public posts
        blog_posts = BlogPost.objects.filter(public = True).order_by('-created_at')
        
        # Forms
        blog_form = BlogForm()
        category_form = CategoryForm()

        # Paginator
        paginator_instance = Paginator(blog_posts, 5)
        page_number = request.GET.get('page')
        posts = paginator_instance.get_page(page_number)

        # Context
        self.context['posts'] = posts
        self.context['blog_form'] = blog_form
        self.context['category_form'] = category_form

        # Return
        return render(request, self.template_name, self.context)



        

# Login function
def blog_login(request):

    # Get user data
    username = request.POST['username']
    password = request.POST['password']

    # Authenticate
    user = authenticate(request, username=username, password=password)
    
    # Return result
    if user is not None:
        login(request, user)
        messages.success(request, 'Login sucessful.')
    else:
        messages.error(request, 'Invalid credentials.')
    
    return redirect("shitblogger:index")
    




# Logout function
def blog_logout(request):
    logout(request)
    return redirect('shitblogger:index')



# Add category
def add_category(request):
    if request.method == 'POST':
        print(request.POST)
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            Category(name = name).save()
            messages.success(request, f'New category {name} added.')
            return redirect('shitblogger:index')
        
        messages.error(request, 'Error during the execution.')
        return redirect('shitblogger:index')



# Add blog post
def add_blog_post(request):
    if request.method == 'POST':
        print(request.POST)
        form = BlogForm(request.POST)
        
        if form.is_valid():
            # Get data
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            categories = form.cleaned_data['categories']
            public = form.cleaned_data['public']
            # Post creation
            post = BlogPost.objects.create(
                        title = title, 
                        content = content, 
                        public = public
                    )
            # Set many-to-many field
            post.categories.set(categories)

            messages.success(request, f'New post {title} added.')
            return redirect('shitblogger:index')
        
        messages.error(request, 'Error during the execution.')
        return redirect('shitblogger:index')
 