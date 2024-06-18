from rest_framework.views import APIView
from .serializers import (UserSerializer, RegisterSerializer)
from rest_framework.response import Response 
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdminOrIsSelf
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes, permission_classes
from django.middleware import csrf
from django.conf import settings

User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
        
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@authentication_classes([])
@permission_classes([AllowAny])
class LoginView(APIView):
    def get(self, request):       
        return Response({
            'detail': 'Provide phone and password to login.'
        }, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        data = request.data
        response = Response()
        phone = data.get('phone', None)
        password = data.get('password', None)
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({"Invalid" : "Invalid phone or password"}, status=status.HTTP_404_NOT_FOUND)
        
        if user.is_active:
            if user.check_password(password):
                tokens = get_tokens_for_user(user)
                access_token = tokens["access"]
                refresh_token = tokens["refresh"]
                # refresh_token
                response.set_cookie(
                    key = "refresh_token",
                    value = refresh_token,
                    expires = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                # access_token
                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
                    value = access_token,
                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                csrf.get_token(request)
                response.data = {"Success" : "Login successfully", "data": tokens}
                return response
            else:
                return Response({"Invalid" : "Invalid phone or password"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"No active" : "This account is not active"}, status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAdminOrIsSelf])
class UserView(APIView):
    """
    get:
    Retrieves information about the current user.

    put:
    Updating information about the current user.
    """
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, username):
        user = get_object_or_404(User, username=username)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@authentication_classes([])
@permission_classes([AllowAny])
class RegisterView(APIView):
    """
    post:
    Register new user.
    """
    def get(self, request):        
        serializer = RegisterSerializer()
        return Response({'serializer': serializer.data})
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            return Response({
                'id': user.pk, 'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': str(user.phone),
                }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
      
class LogoutView(APIView):
    """
    post:
    Logs the user out.
    """
    def post(self, request):
        response = Response({"Success": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token")
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        return response
