from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import UserRegistrationView, profile, UserProfileUpdateView, UserList, UserCreateUpdateDeleteView, BrokerageListCreateView, BrokerageDetailView, UserListCreateView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('user/', profile, name='profile'),
    path('users-list/', UserList.as_view(), name='users-list'),
    path('user/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('users/', UserListCreateView.as_view(), name='user-create-list'),
    path('users/<int:pk>/', UserCreateUpdateDeleteView.as_view(), name='user-detail'),
    path('brokerages/', BrokerageListCreateView.as_view(), name='brokerage-list-create'),
    path('brokerages/<int:pk>/', BrokerageDetailView.as_view(), name='brokerage-detail'),
]
