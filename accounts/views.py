from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions, status
from django.contrib.auth import get_user_model
from rest_framework.decorators import (
    api_view,
)
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from .serializers import CustomUserSerializer
from .models import Brokerage
from .serializers import BrokerageSerializer

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
            'email', 'first_name', 'last_name', 'phone_number',
            'license_number', 'emergency_contact_name',
            'emergency_contact_phone', 'driver_license', 't4a',
            'void_cheque_or_direct_doposite_form', 'annual_commission_statement',
            'deposit_cheque_or_receipt', 'institution_id', 'transit_number',
            'account_number'
        ]
        
        # Handle brokerage separately
        brokerage_id = request.data.get('brokerage')
        if brokerage_id:
            try:
                brokerage = Brokerage.objects.get(id=brokerage_id)
                user.brokerage = brokerage
            except Brokerage.DoesNotExist:
                return Response(
                    {"error": "Invalid brokerage ID"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        for field in allowed_fields:
            if field in request.data:
                if field in ['driver_license', 't4a', 'void_cheque_or_direct_doposite_form', 
                           'annual_commission_statement', 'deposit_cheque_or_receipt']:
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

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class UserCreateUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        if self.kwargs.get('pk'):
            return User.objects.get(pk=self.kwargs['pk'])
        return None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Handle brokerage relationship
        brokerage_id = request.data.get('brokerage')
        if brokerage_id:
            try:
                brokerage = Brokerage.objects.get(id=brokerage_id)
                user = serializer.save(brokerage=brokerage)
            except Brokerage.DoesNotExist:
                return Response(
                    {"error": "Invalid brokerage ID"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            user = serializer.save()
        
        # Set password if provided
        if 'password' in request.data:
            user.set_password(request.data['password'])
            user.save()
            
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Handle brokerage relationship
        brokerage_id = request.data.get('brokerage')
        if brokerage_id:
            try:
                brokerage = Brokerage.objects.get(id=brokerage_id)
                user = serializer.save(brokerage=brokerage)
            except Brokerage.DoesNotExist:
                return Response(
                    {"error": "Invalid brokerage ID"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            user = serializer.save()
        
        # Update password if provided
        if 'password' in request.data:
            user.set_password(request.data['password'])
            user.save()
            
        return Response(serializer.data)

class BrokerageListCreateView(generics.ListCreateAPIView):
    queryset = Brokerage.objects.all()
    serializer_class = BrokerageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BrokerageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brokerage.objects.all()
    serializer_class = BrokerageSerializer
    permission_classes = [IsAuthenticated]