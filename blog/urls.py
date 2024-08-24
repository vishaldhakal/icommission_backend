from django.urls import path
from . import views

urlpatterns = [
      path('category/', views.CategoryListCreateView.as_view(), name='category-list-create'),
      path('category/<int:pk>/', views.CategoryRetrieveUpdateDestroyView.as_view(), name='category-retrieve-update-destroy'),
      path('tag/', views.TagListCreateView.as_view(), name='tag-list-create'),
      path('tag/<int:pk>/', views.TagRetrieveUpdateDestroyView.as_view(), name='tag-retrieve-update-destroy'),
      path('post/', views.PostListCreateView.as_view(), name='post-list-create'),
      path('post/<int:pk>/', views.PostRetrieveUpdateDestroyView.as_view(), name='post-retrieve-update-destroy'),
]
