from email.policy import default
from django.db import models
import uuid
from talent.models import User
from helpers import enum_helper
# Create your models here.
class Hirer(models.Model):
    id = models.UUIDField(primary_key=True, db_column="id",default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

class HirerDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hirer = models.OneToOneField(Hirer, on_delete=models.CASCADE, related_name="hirer")
    company_name = models.CharField(blank=True, null=True, max_length=30)
    location = models.CharField(blank=True, null=True, max_length=100)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    established_on = models.DateField(blank=True, null=True)
    company_size = models.CharField(choices=enum_helper.CompanySize.choices,max_length=100, blank=True, null=True)
    bio = models.CharField(blank=True, null=True, max_length=200)
    profile_photo_url = models.CharField(blank=True, null=True, max_length=200)
    linkedin_url = models.CharField(max_length=100, blank=True, null=True)
    facebook_url = models.CharField(max_length=100, blank=True, null=True)
    instagram_url = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

class Opportunities(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hirer=models.ForeignKey(Hirer, on_delete=models.CASCADE, related_name="hirer_positions")
    role=models.CharField(max_length=50, blank=True, null=True)
    opportunity_type=models.CharField(choices=enum_helper.OpportunityType.choices,max_length=100, blank=True, null=True)
    compensation=models.JSONField(blank=True, null=True)
    expires_at=models.DateTimeField(blank=True, null=True)
    show_to_talent=models.BooleanField(default=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

class Candidature(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    opportunity=models.ForeignKey(Opportunities, on_delete=models.CASCADE, related_name="opportunity")
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="candidate")
    resume_url=models.FileField(blank=True, null=True)
    status=models.CharField(choices=enum_helper.CandidatureStatus.choices,default=enum_helper.CandidatureStatus.APPLIED,max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

