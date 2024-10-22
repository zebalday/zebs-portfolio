from django.contrib import admin
from .models import *

# Models
class AdminBlogPost(admin.ModelAdmin):
    readonly_fields = ('created_at','updated_at')
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    ordering = ('-created_at',)

class AdminCategory(admin.ModelAdmin):
    readonly_fields = ('created_at','updated_at')
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)


# Register
admin.site.register(BlogPost, AdminBlogPost)
admin.site.register(Category, AdminCategory)
