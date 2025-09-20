from users.serializers.account_serializers import (
    LogoutSerializer, 
    ChangePasswordSerializer, 
    RequestEnable2FASerializer, 
    ChangeUsernameSerializer,
    VerifyOTPCode2FSerializer,
    RequestDisable2FASerializer,
    ConfirmDisable2FASerializer,
    RequestChangeEmailSerializer,
    ConfirmChangeEmailSerializer,
    RequestChangeNumber2FASerializer,
    ConfirmOldChangeNumber2FASerializer,
    ConfirmNewChangeNumber2FASerializer
    )

from rest_framework.throttling import ScopedRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response, Serializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from core.send_verification_code import send_otp_code
from core.send_verification_code import send_code_to_email
# from core.verify_code import verify_user_mobile_2FA_code
from django.contrib.auth.models import update_last_login
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging


account_logger = logging.getLogger('users.account')


class LogOutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'logout'

    @swagger_auto_schema(request_body=LogoutSerializer,
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING)]
    )

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = RefreshToken(serializer.validated_data['refresh'])
            refresh_token.blacklist()

            account_logger.info('User %s -  (%s)/ (%s) logout.', request.user.id, request.user.email, request.user.username)
            return Response({
                "message": "successfully logged out."
            }, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            account_logger.warning('failed to logout. Data:  %s Errors: %s', request.data, serializer.errors)
            return Response({str(e)}, status=status.HTTP_400_BAD_REQUEST)



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'change_sensitive'

    @swagger_auto_schema(request_body=ChangePasswordSerializer,
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING)]
    )

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            account_logger.info('User %s -  (%s)/ (%s) changed password successfully.', request.user.id, request.user.email, request.user.username)
            return Response({
                'message': 'password changed successfully.'
            }, status=status.HTTP_200_OK)
        account_logger.warning('failed change passwod. Data:  %s Errors: %s', request.data, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class ChangeUsernameView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'change_sensitive'
    @swagger_auto_schema(request_body=ChangeUsernameSerializer,
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING)]
    )

    def post(self, request):
        serializer = ChangeUsernameSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            account_logger.info('User %s -  (%s)/ (%s) changed useranme successfully.', request.user.id, request.user.email, request.user.username)
            return Response({
                'message': 'Username changed successfully.',
                'username': user.username,
                }, status=status.HTTP_200_OK)
        account_logger.warning('failed change username. Data:  %s Errors: %s', request.data, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RequestEnable2FAView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]    
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'enable2fa_request'

    @swagger_auto_schema(request_body=RequestEnable2FASerializer,
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING)]
    )

    def post(self, request):
        serializer = RequestEnable2FASerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            send_otp_code(user, 'verify_phone')
            account_logger.info('User %s -  (%s)/ (%s) Request to enable 2 factory authenticate.', request.user.id, request.user.email, request.user.username)
            return Response({
                'message': 'OTP code send to user mobile.',
                }, status=status.HTTP_200_OK)
        account_logger.warning('failed Request to enable 2 factory authenticate. Data:  %s Errors: %s', request.data, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyEnable2FAView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'verify_otp'

    @swagger_auto_schema(request_body=VerifyOTPCode2FSerializer,
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING)]
    )
    def post(self, request):
        serializer = VerifyOTPCode2FSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            account_logger.info('User %s -  (%s)/ (%s) confirm enable 2 factory authenticate.', request.user.id, request.user.email, request.user.username)
            return Response({
                'message': '2 factory authenticate enabled successfully.',
            }, status=status.HTTP_200_OK)
        account_logger.warning('failed confirm enable 2 factory authenticate. Data:  %s Errors: %s', request.data, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestDisable2FAView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'disable2fa_request'

    @swagger_auto_schema(request_body=RequestDisable2FASerializer,
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING)]
    )

    def post(self, request):
        serializer = RequestDisable2FASerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            account_logger.info('User %s -  (%s)/ (%s) Request to Disable 2 factory authenticate.', user.id, user.email, user.username)
            return Response({
                "detail": "OTP sent to user mobile.",
                "user": {
                    "id": user.id,
                    "mobile": str(user.mobile),
                }
                }, status=status.HTTP_200_OK)
        account_logger.warning('failed Request to Disable 2 factory authenticate. Data:  %s Errors: %s', request.data, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmDisable2FAView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'verify_otp'

    @swagger_auto_schema(request_body=ConfirmDisable2FASerializer,
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING)]
    )
    def post(self, request):
        serializer = ConfirmDisable2FASerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            account_logger.info('User %s -  (%s)/ (%s) Confirm to Disable 2 factory authenticate.', request.user.id, request.user.email, request.user.username)
            return Response({
                'message': '2 factory authenticate disabled successfully.',
            }, status=status.HTTP_200_OK)
        account_logger.warning('failed confirm to Disable 2 factory authenticate. Data:  %s Errors: %s', request.data, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestChangeEmailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'change_sensitive'

    @swagger_auto_schema(request_body=RequestChangeEmailSerializer,
        manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING)]
    )
    def post(self, request):
        serializer = RequestChangeEmailSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            send_code_to_email(user, 'change_email')
            account_logger.info('User %s -  (%s)/ (%s) Request to change email.', request.user.id, request.user.email, request.user.username)
            return Response({
                'detail': 'Verification code has been send to user email.',
                'user': user.username,
                'new_email': user.pending_email
            }, status=status.HTTP_200_OK)
        account_logger.warning('failed Request to change email. Data:  %s Errors: %s', request.data, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmChangeEmailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'verify_otp'

    @swagger_auto_schema(request_body=ConfirmChangeEmailSerializer,
        manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING)]
    )
    def post(self, request):
        serializer = ConfirmChangeEmailSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            account_logger.info('User %s -  (%s)/ (%s) email changed successfully.', request.user.id, request.user.email, request.user.username)
            return Response({
                'message': 'Email has been changed successfully.',
            }, status=status.HTTP_200_OK)
        account_logger.warning('failed to change email. Data:  %s Errors: %s', request.data, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RequestChangeNumber2FAView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'change_sensitive'

    @swagger_auto_schema(request_body=RequestChangeNumber2FASerializer,
        manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING)]
    )

    def post(self, request):
        serializer = RequestChangeNumber2FASerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        try:
            send_otp_code(request.user, 'verify_phone', send_to_pending=False) # code send to old number
            account_logger.info('User %s -  (%s)/ (%s) Request to change number for 2 FA.', request.user.id, request.user.email, request.user.username)
            return Response({
                'detail': 'OTP has been send to user mobile.',
            }, status=status.HTTP_200_OK)
        except Exception as e:
            account_logger.warning('failed to Request to change number for 2 FA. Data:  %s Errors: %s', request.data, serializer.errors)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ConfirmOldChangeNumber2FAView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'verify_otp'

    @swagger_auto_schema(request_body=ConfirmOldChangeNumber2FASerializer,
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING)]
    )
    def post(self, request):
        serializer = ConfirmOldChangeNumber2FASerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            send_otp_code(user, 'change_number', send_to_pending=True) # code must be send to new mobile number
            account_logger.info('User %s -  (%s)/ (%s) confirm old number of 2 FA.', request.user.id, request.user.email, request.user.username)
            return Response({
                'message': 'OTP has been send to new mobile',
            }, status=status.HTTP_200_OK)
        account_logger.warning('failed to confirm old number of 2 FA. Data:  %s Errors: %s', request.data, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ConfirmNewChangeNumber2FAView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'verify_otp'

    @swagger_auto_schema(request_body=ConfirmNewChangeNumber2FASerializer,
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING)]
    )
    def post(self, request):
        serializer = ConfirmNewChangeNumber2FASerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            account_logger.info('User %s -  (%s)/ (%s) confirm new number of 2 FA and number changed.', request.user.id, request.user.email, request.user.username)
            return Response({
                'message': 'mobile number changed successfully.',
            }, status=status.HTTP_200_OK)
        account_logger.warning('failed to confirm new number of 2 FA. Data:  %s Errors: %s', request.data, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
