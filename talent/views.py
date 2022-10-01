from email.mime import application
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from django.utils.decorators import method_decorator
from .serializers import *
from . import models
from hashlib import sha1
from rest_framework.response import Response
from helpers.api_helper import *
from helpers.enum_helper import *
from helpers.authentication_helper import *
from helpers.auth_helper import login_required
from hirer.models import Opportunities
from hirer.models import Candidature
from hirer.serializers import OpportunityRetrieveSerializer
from helpers.views_helper import *
# Create your views here.
class Registration(APIView):
    @swagger_auto_schema(request_body=CredentialSerializer)
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            try:
                models.User.objects.get(email=email)
                return Response(api_response(ResponseType.FAILED, API_Messages.EMAIL_EXISTS), status=status.HTTP_400_BAD_REQUEST)
            except:
                user=models.User.objects.create(email=email,password=sha1(password.encode()).hexdigest())
                models.UserDetails.objects.create(user=user)
                return Response(api_response(ResponseType.SUCCESS, API_Messages.SUCCESSFUL_REGISTRATION))
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    @swagger_auto_schema(request_body=CredentialSerializer)
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            try:
                user=models.User.objects.get(email=email)
                auth=AuthenticationHelper(user.id)
                auth_response = auth.authentication(user,password)
                if(not auth_response):
                    return Response(api_response(ResponseType.FAILED, API_Messages.INCORRECT_PASSWORD), status=status.HTTP_400_BAD_REQUEST)
                
                access_token = auth.generate_access_token()
                data = {
                    'user': user.id,
                    'email': user.email,
                    'access_token': access_token
                    }
                return Response(api_response(ResponseType.SUCCESS, API_Messages.SUCCESSFUL_LOGIN,data))
            except:
                return Response(api_response(ResponseType.FAILED, API_Messages.EMAIL_DOESNOT_EXIST))
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    def post(self, request):
        try:
            token = request.headers['Authorization'].split(" ")[-1]
            models.TokenBlackList.objects.create(token=token)
            return Response(api_response(ResponseType.SUCCESS, API_Messages.SUCCESSFUL_LOGOUT))
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)

class UserProfile(APIView):
    @swagger_auto_schema(request_body=UserProfileSerializer)
    @method_decorator(login_required(AccountType.TALENT))
    def patch(self, request):
        try:
            serializer = UserProfileSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(api_response(ResponseType.FAILED, serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            data=serializer.data
            user_profile = UserDetails.objects.get(user=request.user)
            user_profile=set_attributes(user_profile,data)
            serializer = UserProfileSerializer(user_profile, many=False)
            return Response(api_response(ResponseType.SUCCESS, API_Messages.PROFILE_UPDATED,serializer.data), status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(login_required(AccountType.TALENT))
    def get(self, request):
        try:
            user_profile = UserDetails.objects.get(user=request.user)
            serializer = UserProfileSerializer(user_profile, many=False)
            return Response(api_response(ResponseType.SUCCESS, API_Messages.USER_PROFILE, serializer.data), status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)

class OpportunityList(APIView):
    @method_decorator(login_required(AccountType.TALENT))
    def get(self, request):
        try:
            query={
                "show_to_talent__exact":True,
                "expires_at__gte":datetime.now(),
            }
            opportunity = Opportunities.objects.filter(Q(**query))
            serializer = OpportunityRetrieveSerializer(opportunity, many=True)
            return Response(api_response(ResponseType.SUCCESS, API_Messages.OPPORTUNITIES, serializer.data), status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)

class Application(APIView):
    @swagger_auto_schema(request_body=CandidatureSerializer)
    @method_decorator(login_required(AccountType.TALENT))
    def patch(self, request,opportunity_id):
        try:
            serializer = CandidatureSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(api_response(ResponseType.FAILED, serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            data=serializer.data
            opportunity = Opportunities.objects.get(id=opportunity_id)
            apply = Candidature.objects.create(user=request.user,opportunity=opportunity)
            apply=set_attributes(apply,data)
            serializer = ApplicationSerializer(apply, many=False)
            return Response(api_response(ResponseType.SUCCESS, API_Messages.APPLIED,serializer.data), status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)

class WithdrawApplication(APIView):
    @method_decorator(login_required(AccountType.TALENT))
    def post(self, request,application_id):
        try:
            apply_record = Candidature.objects.get(id=application_id)
            apply_record.status=CandidatureStatus.WITHDRAWN
            apply_record.save()
            return Response(api_response(ResponseType.SUCCESS, API_Messages.WITHDRAWN), status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)

class Applied(APIView):
    @method_decorator(login_required(AccountType.TALENT))
    def get(self, request):
        try:
            query={
                "user":request.user,
                "status__exact":CandidatureStatus.APPLIED
            }
            applied = Candidature.objects.filter(Q(**query))
            query={
                "user":request.user,
                "status__exact":CandidatureStatus.SELECTED
            }
            selected = Candidature.objects.filter(Q(**query))
            query={
                "user":request.user,
                "status__exact":CandidatureStatus.SHORTLISTED
            }
            shortlisted = Candidature.objects.filter(Q(**query))
            applications=applied.union(selected)
            applications=applications.union(shortlisted)
            serializer = ApplicationSerializer(applications, many=True)
            return Response(api_response(ResponseType.SUCCESS, API_Messages.APPLIED_TO, serializer.data), status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)

class ArchivedApplications(APIView):
    @method_decorator(login_required(AccountType.TALENT))
    def get(self, request):
        try:
            query={
                "user":request.user,
                "status__exact":CandidatureStatus.NOT_CONSIDERED
            }
            not_considered = Candidature.objects.filter(Q(**query))
            query={
                "user":request.user,
                "status__exact":CandidatureStatus.WITHDRAWN
            }
            withdrawn = Candidature.objects.filter(Q(**query))
            applications=not_considered.union(withdrawn)
            serializer = ApplicationSerializer(applications, many=True)
            return Response(api_response(ResponseType.SUCCESS, API_Messages.ARCHIEVED, serializer.data), status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)
