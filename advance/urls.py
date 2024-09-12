from django.urls import path
from . import views

urlpatterns = [
    path('document-notes/', views.DocumentNoteListCreate.as_view(), name='document-note-list-create'),
    path('document-notes/<int:pk>/', views.DocumentNoteRetrieveUpdateDestroy.as_view(), name='document-note-detail'),
    path('documents/', views.DocumentListCreate.as_view(), name='document-list-create'),
    path('documents/<int:pk>/', views.DocumentRetrieveUpdateDestroy.as_view(), name='document-detail'),
    path('commission-advance-requests/', views.CommissionAdvanceRequestListCreate.as_view(), name='commission-advance-request-list-create'),
    path('commission-advance-requests/<int:pk>/', views.CommissionAdvanceRequestRetrieveUpdateDestroy.as_view(), name='commission-advance-request-detail'),
    path('invoice-items/', views.InvoiceItemListCreate.as_view(), name='invoice-item-list-create'),
    path('invoice-items/<int:pk>/', views.InvoiceItemRetrieveUpdateDestroy.as_view(), name='invoice-item-detail'),
    path('invoices/', views.InvoiceListCreate.as_view(), name='invoice-list-create'),
    path('invoices/<int:pk>/', views.InvoiceRetrieveUpdateDestroy.as_view(), name='invoice-detail'),
]