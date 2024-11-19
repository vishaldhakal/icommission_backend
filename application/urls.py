from django.urls import path
from . import views

urlpatterns = [
    path('document-types/', views.get_document_types, name='document-types'),
    path('applications/', views.ApplicationListCreate.as_view(), name='application-list-create'),
    path('applications/<int:pk>/', views.ApplicationRetrieveUpdateDestroy.as_view(), name='application-detail'),
    path('applications/<int:application_id>/documents/', views.DocumentListCreate.as_view(), name='document-list-create'),
    path('documents/<int:pk>/', views.DocumentRetrieveUpdateDestroy.as_view(), name='document-detail'),
    path('documents/<int:document_id>/notes/', views.NoteListCreate.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', views.NoteRetrieveUpdateDestroy.as_view(), name='note-detail'),
    path('applications/<int:application_id>/comments/', views.ApplicationCommentListCreate.as_view(), name='application-comment-list-create'),
    path('comments/<int:pk>/', views.ApplicationCommentRetrieveUpdateDestroy.as_view(), name='application-comment-detail'),
    path('change-requests/', views.ChangeRequestListCreate.as_view(), name='change-request-list-create'),
    path('change-requests/<int:pk>/approve/', views.ChangeRequestApprove.as_view(), name='change-request-approve'),
    path('change-requests/<int:pk>/reject/', views.ChangeRequestReject.as_view(), name='change-request-reject'),
    path('applications/<int:application_id>/change-requests/', views.ApplicationChangeRequestList.as_view(), name='application-change-request-list'),
]
