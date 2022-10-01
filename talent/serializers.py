from .models import *
from rest_framework import serializers
from hirer.models import Candidature

class CredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserDetails
        exclude=('id','user','profile_photo_url','created_at','updated_at')

class CandidatureSerializer(serializers.ModelSerializer):
    class Meta:
        model=Candidature
        fields=('resume_url',)

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Candidature
        fields="__all__"