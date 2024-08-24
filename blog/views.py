from django.shortcuts import render
#django drf generic views
from .models import Tag, Post,Category
from .serializers import CategorySerializer, TagSerializer, PostSerializer
from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework import generics


class CategoryListCreateView(generics.ListCreateAPIView):
      queryset = Category.objects.all()
      serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
      queryset = Category.objects.all()
      serializer_class = CategorySerializer

class TagListCreateView(generics.ListCreateAPIView):
      queryset = Tag.objects.all()
      serializer_class = TagSerializer

class TagRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
      queryset = Tag.objects.all()
      serializer_class = TagSerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        category_id = request.data.get('category')
        tags_data = request.data.get('tags', [])

        # Validate category
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Invalid category ID"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate tags
        tags = []
        for tag_id in tags_data:
            try:
                tag = Tag.objects.get(id=tag_id)
                tags.append(tag)
            except Tag.DoesNotExist:
                return Response({"error": f"Invalid tag ID: {tag_id}"}, status=status.HTTP_400_BAD_REQUEST)

        # Create post
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(category=category)

        # Add tags
        post.tags.set(tags)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        category_id = request.data.get('category')
        tags_data = request.data.get('tags', [])

        # Validate and update category if provided
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                instance.category = category
            except Category.DoesNotExist:
                return Response({"error": "Invalid category ID"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and update tags if provided
        if tags_data:
            tags = []
            for tag_id in tags_data:
                try:
                    tag = Tag.objects.get(id=tag_id)
                    tags.append(tag)
                except Tag.DoesNotExist:
                    return Response({"error": f"Invalid tag ID: {tag_id}"}, status=status.HTTP_400_BAD_REQUEST)
            instance.tags.set(tags)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()