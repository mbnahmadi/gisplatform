from tokenize import TokenError

from django.contrib.auth.password_validation import validate_password
from users.models.two_FA_models import TwoFAModels
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, 
from rest_framework import serializers


User = get_user_model()

class RequestEnable2FA(serializers.Serializer):
    mobile = PhoneNumberField()
    def validate(self, attrs):
        user = self.context['request'].user
        mobile = attrs.get('mobile')
        try:
            user = User.objects.get(user=user)
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found.')




class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.refresh_token = attrs['refresh']
        return attrs



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(wrtie_only=True)
    new_password = serializers.CharField(wrtie_only=True)
    confirm_password = serializers.CharField(wrtie_only=True)

        # user = self.context['request'].user

        # try:
        #     User.objects.filter(user_id=user.id).first()

        # except User.DoesNotExist:
        #     raise serializers.ValidationError('User not found.')
    # def validate_old_password(self, value):
    #     if self.old_password
        

    def validate(self, attrs):
        user = self.context['request'].user

        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError('Old password is wrong.')

        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError('new password and confirm password do not match.')

        validate_password(attrs['new_password'])

        return attrs


    def save(self):
        user = self.context['request'].user
        user.set_password
        