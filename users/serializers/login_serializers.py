from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        identifier = attrs.get('identifier')
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
                'user': user
            }

        return {
            '2FA_required': False,
            'user': user
        }




