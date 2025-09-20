from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers.resetpassword_serializers import ResetPasswordRequestSerializer, ResetPasswordConfirmSerializer
from core.send_verification_code import create_reset_password_link
# from core.verify_code import verify_user_mobile_2FA_code
from django.contrib.auth.models import update_last_login
from drf_yasg.utils import swagger_auto_schema
import logging

resetpassword_logger = logging.getLogger('users.resetpassword')


class ResetPasswordRequestView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'resetpassword_request'
    @swagger_auto_schema(request_body=ResetPasswordRequestSerializer)

    def post(seld, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        try:
            create_reset_password_link(user, request)

            resetpassword_logger.info('User  %s -  (%s)/ (%s) requested to reset password.',  user.id, user.email, user.username)
            return Response({"detail": "Password reset link sent successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            resetpassword_logger.warning('Request reset password failed. Data:  %s Errors: %s', request.data, serializer.errors)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordConfirmView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'verfy_otp'
    @swagger_auto_schema(request_body=ResetPasswordConfirmSerializer)

    def post(seld, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            resetpassword_logger.info('User  %s -  (%s)/ (%s) confirm code and password reset successfully.',  user.id, user.email, user.username)
            return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)

        resetpassword_logger.warning('confirm reset passwird failed. Data:  %s Errors: %s', request.data, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
