from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions, status
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
