import re
from django.core.exceptions import ValidationError
from core.verify_email import verify_user_email
from rest_framework import serializers
from users.models import CustomUserModel
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    '''
    register user with email/username/password fields. (create user)
    '''

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate_password(self, value):
        validate_password(password=value) # با استفاده ازین خط از محدودیت پسورد جنگو که توی ستینگ هست استفاده میکنیم
        return value

    def validate_username(self, value):
        value = value.lower()

        if not re.match(r'^[a-z0-9_]+$', value):
            raise serializers.ValidationError('Username must contain only English letters, numbers or underscore.')

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username already exists.')
        return value
    
    def validate_email(self, value):
        value = value.lower().strip()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email already exists.')
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('password and confirm password do not match.')
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')

        user = User.objects.create_user(
            **validated_data,
            password=password,
            is_active = False,
            is_email_verified = False,
            is_2FA_enabled = False
            )
        
        return user


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    email_code = serializers.CharField()

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        try:
            code = verify_user_email(user, attrs['email_code'], 'verify_email')
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        self.user = user
        self.code = code
        return attrs

    def save(self):
        self.code.is_used = True
        self.code.save(update_fields=['is_used'])
        self.user.is_email_verified = True
        self.user.is_active = True
        self.user.save(update_fields=['is_active', 'is_email_verified'])
        return self.user