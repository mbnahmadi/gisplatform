from users.models.two_FA_models import TwoFAModels
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import get_user_model
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

