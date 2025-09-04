import email
from tokenize import TokenError
from core.verify_code import verify_user_mobile_2FA_code
from django.contrib.auth.password_validation import validate_password
from users.models.two_FA_models import TwoFAModels
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from core.send_verification_code import send_otp_code


User = get_user_model()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.refresh_token = attrs['refresh']
        return attrs



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

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
        user.set_password(self.validated_data['new_password'])
        user.save()
        

class ChangeUsernameSerializer(serializers.Serializer):
    new_username = serializers.CharField()

    def validate(self, attrs):
        value = attrs['new_username'].lower().strip() # strip حذف اسپیس فقط از اول و اخر رشته
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username already exist.')
        return attrs


    def save(self, **kwargs):
        user = self.context['request'].user
        new_username = self.validated_data.get('new_username')

        user.username = new_username
        user.save()
        return user




class ChangeEmailSerializer(serializers.Serializer):
    new_email = serializers.EmailField()

    def validate(self, attrs):
        value = attrs['new_email'].lower().strip() # strip حذف اسپیس فقط از اول و اخر رشته
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email already exist.')
        return attrs


    def save(self, **kwargs):
        user = self.context['request'].user
        new_email = self.validated_data('new_email')

        user.email = new_email
        user.is_email_verified = False
        user.is_active = False
        user.save()
        return user


class RequestEnable2FASerializer(serializers.Serializer):
    mobile = PhoneNumberField()
    def validate(self, attrs):
        mobile = attrs.get('mobile')

        if User.objects.filter(mobile=mobile).exists():
            raise serializers.ValidationError('This mobile already exist.')

        # self.twoFA = twoFA
        return attrs
    
    def save(self):
        mobile = self.validated_data.get('mobile')
        user = self.context['request'].user
        
        user.mobile = mobile
        user.is_2FA_enabled = False
        user.is_mobile_verified = False

        user.save()
        return user
        



class VerifyOTPCode2FSerializer(serializers.Serializer):
    mobile = PhoneNumberField()
    code = serializers.CharField()

    def validate(self, attrs):
        user = self.context['request'].user
        # purpose = self.context['purpose']
        user_mobile = attrs.get('mobile')
        print('user', user)

        try:
            user = User.objects.get(id=user.id)
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found.')
        if not user.mobile == user_mobile:
            # print('user.mobile',user.mobile)
            # print('user_mobile', user_mobile)
            raise serializers.ValidationError('This mobile is not for this user.')
        try:
            otp = verify_user_mobile_2FA_code(user, attrs['code'], 'verify_phone')
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



class RequestDisable2FASerializer(serializers.Serializer):

    def save(self):
        user = self.context['request'].user

        if not user.is_2FA_enabled:
            raise serializers.ValidationError('2FA is already disable.')

        send_otp_code(user, 'Disable_2FA')
        return user


class ConfirmDisable2FASerializer(serializers.Serializer):
    mobile = PhoneNumberField()
    code = serializers.CharField()

    def validate(self, attrs):
        user = self.context['request'].user
        # purpose = self.context['purpose']
        user_mobile = attrs.get('mobile')
        # print('user', user)

        try:
            # print('userrrrrrrr', user)
            user = User.objects.get(id=user.id)
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found.')
        if not user.mobile == user_mobile:
            # print('user.mobile',user.mobile)
            # print('user_mobile', user_mobile)
            raise serializers.ValidationError('This mobile is not for this user.')
        try:
            otp = verify_user_mobile_2FA_code(user, attrs['code'], 'Disable_2FA')
            
        except Exception as e:
            raise serializers.ValidationError(str(e))

        self.otp = otp
        self.user = user
        return attrs

    def save(self):
        self.user.is_2FA_enabled = False
        self.user.mobile = None
        self.user.save()
        self.otp.is_used = True
        self.otp.save(update_fields=['is_used'])
        self.otp.save()

        return self.user






class ChangeNumber2FASerializer(serializers.Serializer):
    pass
