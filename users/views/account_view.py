from users.serializers.account_serializers import LogoutSerializer
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from core.send_verification_code import send_otp_code
# from core.verify_code import verify_user_mobile_2FA_code
from django.contrib.auth.models import update_last_login
from drf_yasg.utils import swagger_auto_schema


class LogOutView(APIView):
    @swagger_auto_schema(request_body=LogoutSerializer)

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = RefreshToken(serializer.validated_data['refresh'])
            refresh_token.blacklist()
            return Response({
                "message": "successfully logged out."
            }, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({str(e)}, status=status.HTTP_400_BAD_REQUEST)
