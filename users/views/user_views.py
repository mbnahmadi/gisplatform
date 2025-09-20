from django.forms import ValidationError
from users.models import CustomUserModel
from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.throttling import ScopedRateThrottle
from drf_yasg.utils import swagger_auto_schema
from core.send_verification_code import send_code_to_email
from users.serializers import RegisterUserSerializer, VerifyEmailSerializer, ResendVerificationCodeSerializer
import logging


register_logger = logging.getLogger('user.register')

User = get_user_model()


class RegisterUserView(APIView):
    # permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'email_register'
    @swagger_auto_schema(request_body=RegisterUserSerializer)

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_code_to_email(user, 'verify_email')

            register_logger.info('User %s -  (%s)/ (%s) register and verification email code send', user.id, user.email, user.username)
            return Response({
                'message': 'The code send to user email.',
                'user_email': user.email,
                }, status=status.HTTP_201_CREATED)

        register_logger.warning('register failed. Data:  %s Errors: %s', request.data, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    # permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'email_verify'
    @swagger_auto_schema(request_body=VerifyEmailSerializer)

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            register_logger.info('User %s -  (%s)/ (%s) verification code confirmed and registered successfilly.', request.user.id, request.user.email, request.user.username)
            return Response({'message': 'user register and verified email.'}, status=status.HTTP_200_OK)

        register_logger.warning('Code verification was rejected. Data:  %s Errors: %s', request.data, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationCodeView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'resend_verification_code'
    @swagger_auto_schema(request_body=ResendVerificationCodeSerializer)

    def post(self, request):
        serializer = ResendVerificationCodeSerializer(data=request.data)
        if serializer.is_valid():

            user = serializer.validated_data['user']

            send_code_to_email(user, 'verify_email')

            register_logger.info('User %s -  (%s)/ (%s) verification code resend successfilly.')
            return Response({
                'message': 'The code send to user email.',
                'user_email': user.email,
                }, status=status.HTTP_201_CREATED)

        register_logger.warning('resending verification code failed. Data:  %s Errors: %s', request.data, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
