from .models import Affiliate, Submission
from rest_framework import serializers


class AffiliateSerializer(serializers.ModelSerializer):
      class Meta:
         model = Affiliate
         fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
      class Meta:
         model = Submission
         fields = '__all__'
         depth = 2