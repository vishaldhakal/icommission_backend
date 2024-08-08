from .models import CommissionAdvanceRequest
from .serializers import CommissionAdvanceRequestSerializer
from rest_framework import generics
class CommissionAdvanceRequestListCreate(generics.ListCreateAPIView):
      queryset = CommissionAdvanceRequest.objects.all()
      serializer_class = CommissionAdvanceRequestSerializer

class CommissionAdvanceRequestDetail(generics.RetrieveUpdateDestroyAPIView):
      queryset = CommissionAdvanceRequest.objects.all()
      serializer_class = CommissionAdvanceRequestSerializer

