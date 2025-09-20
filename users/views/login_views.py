from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers.login_serializers import LoginSerializer, VerifyLoginOTPCode2FSerializer
from core.send_verification_code import send_otp_code
# from core.verify_code import verify_user_mobile_2FA_code
from django.contrib.auth.models import update_last_login
from drf_yasg.utils import swagger_auto_schema
import logging

login_logger = logging.getLogger('users.login')

class LoginView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scoped = 'login'
    @swagger_auto_schema(request_body=LoginSerializer)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            if result['2FA_required']:
                send_otp_code(result['user'], 'Login_2FA')
                # logging
                login_logger.info(f'User %s - (%s)/(%s) attempted login - 2FA required',  result['user'].id, result['user'].email, result['user'].username)
                
                return Response({
                    'message': '2FA OTP code send to user mobile.',
                    'user': result['user_mobile']
                }, status=status.HTTP_200_OK)
           
            user = result['user']
            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)

            # logging
            login_logger.info(f'User %s - (%s)/(%s) logged in successfully (without 2FA)',  user.id, user.email, user.username)
            return Response({
                'token':{
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                },
                'user': {
                    'id': user.id,
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)
            
        # logging
        login_logger.warning('Login failed. Data:  %s Errors: %s', request.data, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                

class VerifyLoginOTPCode2FAView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scoped = 'verfy_otp'
    @swagger_auto_schema(request_body=VerifyLoginOTPCode2FSerializer)

    def post(self, request):
        serializer = VerifyLoginOTPCode2FSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)

            login_logger.info(f'User %s - (%s)/(%s) logged in successfully (with 2FA)',  user.id, user.email, user.username)
            return Response({
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                },
                'user': {
                    'id': user.id,
                    'email': user.email
                }
            }, status=status.HTTP_200_OK)

        login_logger.warning('verification code error. Data:  %s Errors: %s', request.data, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        