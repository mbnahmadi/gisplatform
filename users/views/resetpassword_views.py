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


class ResetPasswordRequestView(APIView):
    @swagger_auto_schema(request_body=ResetPasswordRequestSerializer)

    def post(seld, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        try:
            create_reset_password_link(user, request)
            return Response({"detail": "Password reset link sent successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordConfirmView(APIView):
    @swagger_auto_schema(request_body=ResetPasswordConfirmSerializer)

    def post(seld, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
