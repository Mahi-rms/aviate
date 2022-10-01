from .models import *
from rest_framework import serializers


class HirerCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

class HirerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=HirerDetails
        exclude=('id','hirer','profile_photo_url','created_at','updated_at')

class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model=Opportunities
        exclude=('id','hirer','created_at','updated_at')

class OpportunityRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model=Opportunities
        fields="__all__"