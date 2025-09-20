import logging
from django.contrib.auth import get_user_model
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response, Serializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers.profile_serializers import ProfileUpdateSerializer
from django.contrib.auth.models import update_last_login
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging


profile_logger = logging.getLogger('users.profile')


User = get_user_model()

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'profile'
    parser_classes = (MultiPartParser, FormParser) # باعث میشه request.data و request.FILES باهم ارسال بشن
# request_body=ProfileUpdateSerializer,
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
            openapi.Parameter('first_name', openapi.IN_FORM, description='first name', type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('last_name', openapi.IN_FORM, description='last name', type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('profile_image_uploaded', openapi.IN_FORM, description='Profile image file', type=openapi.TYPE_FILE, required=False),
            openapi.Parameter('remove_profile_image', openapi.IN_FORM, description='Set true to remove profile image', type=openapi.TYPE_BOOLEAN, required=False),
        ]
    )

    def put(self, request):
        # partial باعث میشه نخوایم همه فیلد هارو بفرستیم
        serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=True, context={'request': request})
        # print(request.data)
        if serializer.is_valid():
            serializer.save()
            # profile_logger.info(f'User {request.user.id} - ({request.user.email})/({request.user.username}) changed profile.')
            profile_logger.info('User %s -  (%s)/ (%s) changed profile.', request.user.id, request.user.email, request.user.username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        profile_logger.warning('cahnge profile data failed. Data:  %s Errors: %s', request.data, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING)]
    )
    def get(self, request):
        serializer = ProfileUpdateSerializer(request.user, context={'request': request})

        # profile_logger.info(f'User {request.user.id} - ({request.user.email})/({request.user.username}) see profile.')
        profile_logger.info('User %s -  (%s)/ (%s) see profile.', request.user.id, request.user.email, request.user.username)
        return Response({
            'user_profile': serializer.data
        }, status=status.HTTP_200_OK)

        
