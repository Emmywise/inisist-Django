from django.shortcuts import render
from rest_framework import status, generics
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authtoken.serializers import AuthTokenSerializer
# Create your views here.

class RegisterView(generics.GenericAPIView): # user register view
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.save()
        return Response({           #to get an objectlike response
            "user": RegisterSerializer(user_data, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user_data)[1]
        })

class LoginApi(KnoxLoginView):  # user Login view
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginApi, self).post(request, format=None)
