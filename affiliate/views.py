from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Affiliate, Submission
from .serializers import SubmissionSerializer, AffiliateSerializer
from django.db.models import Count
from rest_framework import generics

class AffiliateListCreate(generics.ListCreateAPIView):
    queryset = Affiliate.objects.all()
    serializer_class = AffiliateSerializer

class AffiliateRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Affiliate.objects.all()
    serializer_class = AffiliateSerializer

class SubmissionListCreate(generics.ListCreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

class SubmissionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

@api_view(['POST'])
def submit_form(request):
   affiliate_id = request.data.get('affiliate_id')
   name = request.data.get('name')
   email = request.data.get('email')
   phone = request.data.get('phone')
   message = request.data.get('message')

   try:
      affiliate = Affiliate.objects.get(id=affiliate_id)
      Submission.objects.create(
         affiliate=affiliate,
         name=name,
         email=email,
         phone=phone,
         message=message
      )
      return Response({'success': 'Form submitted successfully'})
      
   except Affiliate.DoesNotExist:
      return Response({'error': 'Invalid affiliate ID'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def verify_affiliate(request):
    affiliate_id = request.query_params.get('id')
    try:
        affiliate = Affiliate.objects.get(id=affiliate_id)
        serializer = AffiliateSerializer(affiliate)
        return Response({'valid': True, 'affiliate': serializer.data},status=status.HTTP_200_OK)
    except Affiliate.DoesNotExist:
        return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def all_submissions(request):
    submissions = Submission.objects.all()
    serializer = SubmissionSerializer(submissions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_affiliate_submissions(request, affiliate_id):
    try:
        affiliate = Affiliate.objects.get(id=affiliate_id)
        submissions = Submission.objects.filter(affiliate=affiliate)
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)
    except Affiliate.DoesNotExist:
        return Response({'error': 'Affiliate not found'}, status=status.HTTP_404_NOT_FOUND)