from django.urls import path
from . import views

urlpatterns = [
    path('applications/', views.ApplicationListCreate.as_view(), name='application-list-create'),
    path('applications/<int:pk>/', views.ApplicationRetrieveUpdateDestroy.as_view(), name='application-detail'),
    path('applications/<int:application_id>/documents/', views.DocumentListCreate.as_view(), name='document-list-create'),
    path('documents/<int:pk>/', views.DocumentRetrieveUpdateDestroy.as_view(), name='document-detail'),
    path('documents/<int:document_id>/notes/', views.NoteListCreate.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', views.NoteRetrieveUpdateDestroy.as_view(), name='note-detail'),
    path('applications/<int:application_id>/comments/', views.ApplicationCommentListCreate.as_view(), name='application-comment-list-create'),
    path('comments/<int:pk>/', views.ApplicationCommentRetrieveUpdateDestroy.as_view(), name='application-comment-detail'),
]