from django.urls import path
from . import views

urlpatterns = [
   path('submit-form/', views.submit_form, name='submit_form'),
   path('verify-affiliate/', views.verify_affiliate, name='verify_affiliate'),
   path('all-submissions/', views.all_submissions, name='all_submissions'),
   path('affiliates/', views.AffiliateListCreate.as_view(), name='affiliate-list-create'),
   path('affiliates/<int:pk>/', views.AffiliateRetrieveUpdateDestroy.as_view(), name='affiliate-detail'),
   path('affiliate-submissions/<int:affiliate_id>/', views.get_affiliate_submissions, name='affiliate-submissions'),
   path('submissions/', views.SubmissionListCreate.as_view(), name='submission-list-create'),
   path('submissions/<int:pk>/', views.SubmissionRetrieveUpdateDestroy.as_view(), name='submission-detail'),
]

