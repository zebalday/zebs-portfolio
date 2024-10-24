from rest_framework.serializers import ModelSerializer
from .models import BlogPost

class BlogPostSerializer(ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'