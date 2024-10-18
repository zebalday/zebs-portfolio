from django.contrib import admin
from .models import Project

# Models
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'github_url', 'deploy_url', 'thumbnail') 
    search_fields = ('name',)
    ordering = ('-name',)


# Register your models here.
admin.site.register(Project, ProjectAdmin)

# Admin site config
title = 'ZEBS PORTFOLIO'
subtitle = 'Admin Panel'
admin.site.index_title = title
admin.site.site_header = subtitle
admin.site.site_title = subtitle

