from django.urls import path
from .views import PartnerListCreateView, PartnerRetrieveUpdateDestroyView

urlpatterns = [
    path('partners/', PartnerListCreateView.as_view(), name='partner-list-create'),
    path('partners/<int:pk>/', PartnerRetrieveUpdateDestroyView.as_view(), name='partner-retrieve-update-destroy'),
]