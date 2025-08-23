from users.serializers.account_serializers import LogoutSerializer, ChangePasswordSerializer, RequestEnable2FASerializer, ChangeUsernameSerializer
from users.serializers.login_serializers import VerifyOTPCode2FSerializer
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



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(request_body=ChangePasswordSerializer,
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING)]
    )

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'password changed successfully.'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class ChangeUsernameView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(request_body=ChangeUsernameSerializer,
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING)]
    )

    def post(self, request):
        serializer = ChangeUsernameSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Username changed successfully.',
                'username': user.username,
                }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RequestEnable2FAView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(request_body=RequestEnable2FASerializer,
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING)]
    )

    def post(self, request):
        serializer = RequestEnable2FASerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            mobile = serializer.validated_data['mobile']
            send_otp_code(request.user, mobile, 'verify_phone')
            return Response({
                'message': 'OTP code send to user mobile.',
                }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyEnable2FAView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(request_body=VerifyOTPCode2FSerializer,
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING)]
    )
    def post(self, request):
        serializer = VerifyOTPCode2FSerializer(data=request.data, context={'request': request, 'purpose': 'verify_phone'})
        if serializer.is_valid():
            serializer.save()
            # refresh = RefreshToken.for_user(user)
            # update_last_login(None, user)
            return Response({
                'message': '2 factory authenticate enabled successfully.',
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)