from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from django.db.models import Q
from helpers.views_helper import set_attributes
from .serializers import *
from . import models
from hashlib import sha1
from rest_framework.response import Response
from helpers.api_helper import *
from helpers.enum_helper import *
from helpers.authentication_helper import *
from helpers.auth_helper import login_required
# Create your views here.
class HirerRegistration(APIView):
    @swagger_auto_schema(request_body=HirerCredentialSerializer)
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            try:
                models.Hirer.objects.get(email=email)
                return Response(api_response(ResponseType.FAILED, API_Messages.EMAIL_EXISTS), status=status.HTTP_400_BAD_REQUEST)
            except:
                hirer=models.Hirer.objects.create(email=email,password=sha1(password.encode()).hexdigest())
                models.HirerDetails.objects.create(hirer=hirer)
                return Response(api_response(ResponseType.SUCCESS, API_Messages.SUCCESSFUL_REGISTRATION))
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)


class HirerLogin(APIView):
    @swagger_auto_schema(request_body=HirerCredentialSerializer)
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            try:
                hirer=models.Hirer.objects.get(email=email)
                auth=AuthenticationHelper(hirer.id)
                auth_response = auth.authentication(hirer,password)
                if(not auth_response):
                    return Response(api_response(ResponseType.FAILED, API_Messages.INCORRECT_PASSWORD), status=status.HTTP_400_BAD_REQUEST)
                
                access_token = auth.generate_access_token()
                data = {
                    'hirer': hirer.id,
                    'email': hirer.email,
                    'access_token': access_token
                    }
                return Response(api_response(ResponseType.SUCCESS, API_Messages.SUCCESSFUL_LOGIN,data))
            except:
                return Response(api_response(ResponseType.FAILED, API_Messages.EMAIL_DOESNOT_EXIST))
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)

class HirerLogout(APIView):
    def post(self, request):
        try:
            token = request.headers['Authorization'].split(" ")[-1]
            models.TokenBlackList.objects.create(token=token)
            return Response(api_response(ResponseType.SUCCESS, API_Messages.SUCCESSFUL_LOGOUT))
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)

class HirerProfile(APIView):
    @swagger_auto_schema(request_body=HirerProfileSerializer)
    @method_decorator(login_required(AccountType.HIRER))
    def patch(self, request):
        try:
            serializer = HirerProfileSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(api_response(ResponseType.FAILED, serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            data=serializer.data
            hirer_profile = HirerDetails.objects.get(hirer=request.hirer)
            set_attributes(hirer_profile,data)
            serializer = HirerProfileSerializer(hirer_profile, many=False)
            return Response(api_response(ResponseType.SUCCESS, API_Messages.PROFILE_UPDATED,serializer.data), status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(login_required(AccountType.HIRER))
    def get(self, request):
        try:
            hirer_profile = HirerDetails.objects.get(hirer=request.hirer)
            serializer = HirerProfileSerializer(hirer_profile, many=False)
            return Response(api_response(ResponseType.SUCCESS, API_Messages.HIRER_PROFILE, serializer.data), status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)

class HiringList(APIView):
    @swagger_auto_schema(request_body=OpportunitySerializer)
    @method_decorator(login_required(AccountType.HIRER))
    def patch(self, request):
        try:
            id=""
            if('id' in request.data):
                id=request.data['id']
                del request.data['id']
            serializer = OpportunitySerializer(data=request.data)
            if not serializer.is_valid():
                return Response(api_response(ResponseType.FAILED, serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            data=serializer.data
            if(len(id)):
                opportunity = Opportunities.objects.create(id=id)
                opportunity=set_attributes(opportunity,data)
                serializer = OpportunitySerializer(opportunity, many=False)
                return Response(api_response(ResponseType.SUCCESS, API_Messages.UPDATED_OPPORTUNITY,serializer.data), status=status.HTTP_200_OK)
            
            opportunity = Opportunities.objects.create(hirer=request.hirer)
            set_attributes(opportunity,data)
            serializer = OpportunitySerializer(opportunity, many=False)
            return Response(api_response(ResponseType.SUCCESS, API_Messages.ADDED_OPPORTUNITY,serializer.data), status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(login_required(AccountType.HIRER))
    def get(self, request):
        try:
            opportunity = Opportunities.objects.filter(Q(**{"hirer":request.hirer}))
            print(opportunity)
            serializer = OpportunitySerializer(opportunity, many=True)
            return Response(api_response(ResponseType.SUCCESS, API_Messages.OPPORTUNITIES, serializer.data), status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)
