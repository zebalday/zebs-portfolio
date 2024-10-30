from django.db import models

# CATEGORY
class Category(models.Model):
    name = models.CharField(
        verbose_name='Title',
        max_length=60,
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(
        verbose_name='Created at',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Updated at',
        auto_now=True
    )
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['-created_at']

    def __str__(self):
        return (self.name)

# BLOG POST
class BlogPost(models.Model):

    title = models.CharField(
        verbose_name='Title',
        max_length=60,
        null=False,
        blank=False
    )
    content = models.CharField(
        verbose_name='Post Content',
        max_length=450,
        null=False,
        blank=False
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name='Categories',
        null=True,
        blank=True
    )
    public = models.BooleanField(
        verbose_name='Show post?',
        default=True
    )
    created_at = models.DateTimeField(
        verbose_name='Created at',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Updated at',
        auto_now=True
    )

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

    def __str__(self):
        return (self.title)

