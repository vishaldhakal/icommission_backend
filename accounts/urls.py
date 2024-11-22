from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import UserRegistrationView, profile, UserProfileUpdateView, UserList

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('user/', profile, name='profile'),
    path('users-list/', UserList.as_view(), name='users-list'),
    path('user/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
]
