from django.urls import path
from . import views

urlpatterns = [
   path('submit-form/', views.submit_form, name='submit_form'),
   path('verify-affiliate/', views.verify_affiliate, name='verify_affiliate'),
   path('all-submissions/', views.all_submissions, name='all_submissions'),
]

