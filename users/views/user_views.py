from users.models import CustomUserModel
from core.send_verification_code import send_code_to_email
from users.serializers import RegisterUserSerializer, VerifyEmailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()


class RegisterUserView(APIView):
    # permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=RegisterUserSerializer)

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_code_to_email(user, 'verify_email')
            return Response({
                'message': 'The code send to user email.',
                'user_email': user.email,
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    # permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=VerifyEmailSerializer)

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'user register and verified email.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)