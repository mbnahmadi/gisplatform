from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.serializers import serialize
from drf_yasg.utils import APIView, swagger_auto_schema
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from core.verify_code import verify_user_mobile_2FA_code
from users.models.two_FA_models import TwoFAModels

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        identifier = attrs.get('identifier').lower().strip()
        password = attrs.get('password')

        user = authenticate(username=identifier, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_active:
            raise serializers.ValidationError('User is not active.')
        if not user.is_email_verified:
            raise serializers.ValidationError('User email is not active. please first active your email')

        self.user = user
        return attrs

    def save(self):
        user = self.user
        if user.is_2FA_enabled:
            # send_otp_code(user, 'login_2FA_OTP') 
            return {
                '2FA_required': True,
                'user': user,
                'user_mobile': str(user.mobile)
            }

        return {
            '2FA_required': False,
            'user': user
        }


        

class VerifyLoginOTPCode2FSerializer(serializers.Serializer):
    mobile = PhoneNumberField()
    code = serializers.CharField()

    def validate(self, attrs):
        # user = self.context['request'].user
        user_mobile = attrs.get('mobile')
        print('user_mobile', user_mobile)

        try:
            user = User.objects.get(mobile=user_mobile)
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found.')
        # if not user.mobile == user_mobile:
        #     # print('user.mobile',user.mobile)
        #     # print('user_mobile', user_mobile)
        #     raise serializers.ValidationError('This mobile is not for this user.')
        try:
            otp = verify_user_mobile_2FA_code(user, attrs['code'], 'Login_2FA')
        except Exception as e:
            raise serializers.ValidationError(str(e))

        self.otp = otp
        self.user = user
        return attrs

    def save(self):
        self.user.is_2FA_enabled = True
        self.user.is_mobile_verified = True
        self.user.save()
        self.otp.is_used = True
        self.otp.save(update_fields=['is_used'])
        self.otp.save()

        return self.user

