from django.urls import path
from . import views

urlpatterns = [
   path('advance-request/', views.CommissionAdvanceRequestListCreate.as_view()),
   path('advance-request/<int:pk>/', views.CommissionAdvanceRequestDetail.as_view()),
]
