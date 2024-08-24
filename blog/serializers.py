from .models import Post, Category, Tag
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
      class Meta:
         model = Category
         fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
      class Meta:
         model = Tag
         fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
      class Meta:
         model = Post
         fields = '__all__'