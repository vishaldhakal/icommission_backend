from django.urls import path
from .views import ApplicationListCreateView, ApplicationRetrieveUpdateDestroyView

urlpatterns = [
    path('applications/', ApplicationListCreateView.as_view(), name='application-list-create'),
    path('applications/<int:pk>/', ApplicationRetrieveUpdateDestroyView.as_view(), name='application-detail'),
]