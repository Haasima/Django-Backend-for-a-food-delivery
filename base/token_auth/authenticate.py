from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response 
import logging

User = get_user_model()

logger = logging.getLogger(__name__)

class PhoneAuthBackends:
    """
    Phone Authentication 
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(phone=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def enforce_csrf(request):
    """
    Enforce CSRF validation.
    """
    check = CSRFCheck(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)

class CustomAuthentication(JWTAuthentication):
    def authenticate(self, request: Request):
        logger.debug("Starting authentication process.")
        
        header = self.get_header(request)
        logger.debug(f"Header: {header}")
        
        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
            logger.debug(f"Raw token from cookies: {raw_token}")
        else:
            raw_token = self.get_raw_token(header=header)
            logger.debug(f"Raw token from header: {raw_token}")
            
        if raw_token is None:
            logger.debug("No raw token found.")
            return None
        
        validated_token = None
        
        try:
            logger.debug('Try to validate token')
            validated_token = self.get_validated_token(raw_token)
            logger.debug(f"Validated token: {validated_token}")
        except InvalidToken:
            # Access token has expired, try to refresh it
            logger.debug('Access token has expired, trying to refresh')
            refresh_token = request.COOKIES.get('refresh_token')
            logger.debug(f"refresh_token from cookies: {str(refresh_token)}")
            if refresh_token is None:
                logger.error("No refresh token provided.")
                raise AuthenticationFailed('No valid refresh token provided.')
            try:
                refresh_token = RefreshToken(refresh_token)
                new_access_token = refresh_token.access_token
                logger.debug(f"new_access_token created: {str(new_access_token)}")
                response = Response()
                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
                    value = new_access_token,
                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                logger.debug(f"Set new access token in cookie: {str(new_access_token)}")
                validated_token = self.get_validated_token(str(new_access_token))
                logger.debug(f"New validated token: {validated_token}")
            except TokenError as e:
                logger.debug(f"Token error: {str(e)}")
                raise AuthenticationFailed('Invalid refresh token.')
        
        enforce_csrf(request=request)
        logger.debug("CSRF check passed.")
        return self.get_user(validated_token=validated_token), validated_token