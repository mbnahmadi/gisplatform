from django.contrib.auth import get_user_model
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response, Serializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers.profile_serializers import ProfileUpdateSerializer, GetProfileSerializer
from django.contrib.auth.models import update_last_login
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


User = get_user_model()

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
# request_body=ProfileUpdateSerializer,
    @swagger_auto_schema(
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING)]
    )

    # def put(self, request):
    #     pass


    def get(self, request):
        try:
            print(request.user)
            user_profile = User.objects.get(username=request.user)
            print(user_profile)
            serializer = GetProfileSerializer(user_profile)
            return Response({
                'user_profile': serializer.data
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
