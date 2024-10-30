from .models import *
from django.forms import ModelForm
from django import forms

# Blog form
class BlogForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'categories', 'public',]
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-input', 'placeholder':'Post title'}),
            'content' : forms.Textarea(attrs={'class':'form-input', 'placeholder':'Post content', 'resize':'none'}),
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
            'name' : forms.TextInput(attrs={'class':'form-input', 'placeholder':'Category name'})
        }
        labels = {
            'name':False,
        }


