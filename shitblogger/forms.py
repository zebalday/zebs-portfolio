from .models import *
from django.forms import ModelForm

# Blog form
class BlogForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'categories', 'public',]
        widgets = {
            'title' : models.TextField(attrs={'class':'form-imput', 'placeholder':'Post title'}),
            'content' : models.TextField(attrs={'class':'form-imput', 'placeholder':'Post content'}),
        }
        labels = {
            'title':False,
            'content':False
        }


# Category
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name' : models.TextField(attrs={'class':'form-imput', 'placeholder':'Category name'})
        }
        labels = {
            'name':False,
        }

