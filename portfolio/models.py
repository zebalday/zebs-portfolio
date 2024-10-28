from django.db import models

# Create your models here.

class Project(models.Model):
    
    name = models.CharField(
        verbose_name = 'Project Name',
        max_length = 40,
        null = False,
        default = 'Default name'
    )
    description = models.CharField(
        verbose_name = 'Project Description',
        max_length = 100,
        null = False,
        default = 'Default description'
    )
    thumbnail = models.ImageField(
        verbose_name = 'Project Thumbnail',
        upload_to = 'project_thumbnails',
        null = True,
        blank = True
    )
    github_url = models.URLField(
        verbose_name = 'Project Github',
        max_length = 200,
        null = True,
        blank = True
    )
    deploy_url = models.URLField(
        verbose_name = 'Project Deploy Link',
        max_length = 300,
        null = True,
        blank = True
    )
    public = models.BooleanField(
        verbose_name = 'Show this Project?',
        editable = True,
        default = False
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.github_url})"


class SpotifyToken(models.Model):
    token_type = models.CharField(max_length=50)
    access_token = models.CharField(max_length=300)
    refresh_token = models.CharField(max_length=300)
    expires_in = models.DateTimeField()
    scope = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return (f"{self.updated_at}\n{self.access_token}\n{self.refresh_token}")