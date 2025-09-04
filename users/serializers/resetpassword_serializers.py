from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from users.models import ResetPasswordTokenModel
from core.verify_code import verify_reset_password_link
from users.models.profile_models import ProfileModel


User = get_user_model()

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        value = value.lower().strip()
        user = User.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError('User with this email not found.')
        if not user.is_active:
            raise serializers.ValidationError(_('This user account is inactive.'))
        self.user = user
        return value

    
class ResetPasswordConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(password=value)
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError('Passwords do not match.')
        try:
            user = verify_reset_password_link(attrs['token'])
            self.user = user
        except ValidationError as e:
            raise serializers.ValidationError({"token": str(e)})
        
        return attrs


    def save(self):
        self.user.set_password(self.validated_data['new_password'])
        self.user.save(update_fields=['password'])
        return self.user


