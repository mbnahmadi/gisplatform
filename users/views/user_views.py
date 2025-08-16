from urllib3 import response
from users.models import CustomUserModel
from users.serializers import RegisterUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class RegisterUserView(APIView):
    @swagger_auto_schema(request_body=RegisterUserSerializer)

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # send_code_to_verify_email
            return Response({'message': 'The code send to user email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)