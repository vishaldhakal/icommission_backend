from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions, status
from django.contrib.auth import get_user_model
from rest_framework.decorators import (
    api_view,
    parser_classes,
)
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from .serializers import CustomUserSerializer
from .models import Brokerage
from .serializers import BrokerageSerializer
from rest_framework.parsers import MultiPartParser
import csv
from io import StringIO
from django.db import transaction

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

@api_view(['POST'])
@parser_classes([MultiPartParser])
def bulk_upload_brokerages(request):
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No file provided'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    file = request.FILES['file']
    if not file.name.endswith('.csv'):
        return Response(
            {'error': 'File must be a CSV'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        decoded_file = file.read().decode('utf-8-sig')  # Handle BOM
        reader = csv.DictReader(StringIO(decoded_file))
        
        with transaction.atomic():
            created_count = 0
            updated_count = 0
            errors = []
            
            for row_number, row in enumerate(reader, start=2):
                try:
                    # Map CSV columns to model fields
                    brokerage_data = {
                        'city': row.get('City', '').strip() or None,
                        'province': row.get('Province', '').strip() or None,
                        'company_name': row.get('Company Name', '').strip(),
                        'broker_of_record': row.get('BoR or Managing Broker', '').strip() or None,
                        'broker_email': row.get('Broker Email', '').strip() or None,
                        'deal_administrator_name': row.get('Deal Administrator Name', '').strip() or None,
                        'deal_administrator_email': row.get('Deal Administrator Email', '').strip() or None,
                        'notes': row.get('Notes', '').strip() or None,
                        'account_manager': row.get('Account Manager', '').strip() or None,
                        'stage': row.get('Stages', '').strip() or 'Prospect'
                    }

                    # Only validate company_name as required
                    if not brokerage_data['company_name']:
                        errors.append(f"Row {row_number}: Missing required field: company_name")
                        continue

                    # Map stages to model choices
                    stage_mapping = {
                        'Running': 'Running',
                        'Work in progress': 'Work In Progress',
                        'Lost': 'Lost',
                        'Prospect': 'Prospect',
                        'Other': 'Other'
                    }
                    brokerage_data['stage'] = stage_mapping.get(brokerage_data['stage'], 'Prospect')

                    # Try to update existing brokerage or create new one
                    try:
                        brokerage = Brokerage.objects.get(company_name=brokerage_data['company_name'])
                        for key, value in brokerage_data.items():
                            if value is not None:  # Only update non-None values
                                setattr(brokerage, key, value)
                        brokerage.save()
                        updated_count += 1
                    except Brokerage.DoesNotExist:
                        Brokerage.objects.create(**brokerage_data)
                        created_count += 1

                except Exception as e:
                    errors.append(f"Row {row_number}: {str(e)}")

            # Update agent counts after all brokerages are created/updated
            for brokerage in Brokerage.objects.all():
                brokerage.update_agent_count()

            response_data = {
                'message': 'Import completed',
                'created': created_count,
                'updated': updated_count,
                'errors': errors
            }

            if errors:
                response_data['status'] = 'completed_with_errors'
                return Response(response_data, status=status.HTTP_200_OK)  # Changed to 200 since partial success is OK

            return Response(response_data, status=status.HTTP_200_OK)

    except UnicodeDecodeError:
        return Response(
            {'error': 'Invalid file encoding. Please use UTF-8.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'Error processing file: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )