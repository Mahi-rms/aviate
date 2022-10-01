from django.db import models
import uuid
from helpers import enum_helper
# Create your models here.
class User(models.Model):
    id = models.UUIDField(primary_key=True, db_column="id",default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

class UserDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    first_name = models.CharField(blank=True, null=True, max_length=30)
    last_name = models.CharField(blank=True, null=True, max_length=30)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(choices=enum_helper.Gender.choices, blank=True, null=True, max_length=30)
    bio = models.CharField(blank=True, null=True, max_length=200)
    profile_photo_url = models.CharField(blank=True, null=True, max_length=200)
    linkedin_profile = models.CharField(max_length=100, blank=True, null=True)
    facebook_profile = models.CharField(max_length=100, blank=True, null=True)
    instagram_profile = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

class UserEducation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_ed")
    institution_name=models.CharField(blank=True, null=True, max_length=50)
    qualification=models.CharField(choices=enum_helper.Qualification.choices, blank=True, null=True, max_length=50)
    start=models.DateField(blank=True,null=True)
    end=models.DateField(blank=True,null=True)
    score_type=models.CharField(choices=enum_helper.ScoreType.choices, blank=True, null=True, max_length=50)
    score=models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

class TokenBlackList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token=models.CharField(max_length=150, blank=True, null=True)
    expiry=models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
