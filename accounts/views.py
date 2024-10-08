from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.decorators import (
    api_view,
)
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

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
        # Only update specific fields
        allowed_fields = [
            'broker_of_record_email', 'broker_of_record_name', 'brokerage_phone',
            'current_brokerage_name', 'driver_license', 'email',
            'emergency_contact_name', 'emergency_contact_phone', 'first_name',
            'last_name', 'license_number', 'phone_number', 'role', 'deal_administrator_name', 'deal_administrator_email'
        ]
        
        # Update the user object with the allowed fields
        for field in allowed_fields:
            if field in request.data:
                if field == 'driver_license':
                    if request.FILES.get(field):
                        user.driver_license = request.FILES[field]
                    elif request.data[field] is None:
                        user.driver_license = None
                else:
                    setattr(user, field, request.data[field])
        
        # Save the updated user object
        user.save()

        # Return the updated user object
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        

@api_view(['GET'])
def profile(request):
    if request.method == 'GET':
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)