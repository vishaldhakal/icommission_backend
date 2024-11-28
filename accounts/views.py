from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions, status
from django.contrib.auth import get_user_model
from rest_framework.decorators import (
    api_view,
)
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount.models import SocialAccount
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
import json
import requests

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

#view for updating user profile
class UserProfileUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        allowed_fields = [
            'broker_of_record_email', 'broker_of_record_name', 'brokerage_phone',
            'current_brokerage_name', 'driver_license', 'email',
            'emergency_contact_name', 'emergency_contact_phone', 'first_name',
            'last_name', 'license_number', 'phone_number', 'role', 
            'deal_administrator_name', 'deal_administrator_email',
            't4a', 'void_cheque_or_direct_doposite_form',
            'annual_commission_statement', 'deposit_cheque_or_receipt',
            'institution_id', 'transit_number', 'account_number'
        ]
        
        for field in allowed_fields:
            if field in request.data:
                if field in ['driver_license', 't4a', 'void_cheque_or_direct_doposite_form', 'annual_commission_statement', 'deposit_cheque_or_receipt']:
                    if request.FILES.get(field):
                        setattr(user, field, request.FILES[field])
                    elif request.data[field] is None:
                        setattr(user, field, None)
                else:
                    setattr(user, field, request.data[field])
        
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

@api_view(['GET'])
def profile(request):
    if request.method == 'GET':
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:3000'
    client_class = OAuth2Client

    def create_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }

    def post(self, request, *args, **kwargs):
        try:
            access_token = request.data.get('access_token')
            if not access_token:
                return Response(
                    {'error': 'No access token provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get user info from Google using the access token
            google_response = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                headers={'Authorization': f'Bearer {access_token}'}
            )

            if not google_response.ok:
                return Response(
                    {'error': 'Failed to get user info from Google'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            google_data = google_response.json()

            # Extract user information
            email = google_data.get('email')
            if not email:
                return Response(
                    {'error': 'Email not provided by Google'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Try to find existing user by email
            try:
                user = User.objects.get(email=email)
                # Update user info if needed
                if not user.first_name:
                    user.first_name = google_data.get('given_name', '')
                if not user.last_name:
                    user.last_name = google_data.get('family_name', '')
                user.save()
            except User.DoesNotExist:
                # Create new user
                username = email  # Use email as username
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=google_data.get('given_name', ''),
                    last_name=google_data.get('family_name', ''),
                    role='Agent',  # Default role
                    password=None  # No password for social auth
                )

            # Generate tokens
            tokens = self.create_token(user)
            return Response(tokens, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error in Google Login: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )