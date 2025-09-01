from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.serializers import serialize
from drf_yasg.utils import APIView, swagger_auto_schema
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from core.verify_code import verify_user_mobile_2FA_code
from users.models.profile_models import ProfileModel


User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField() # برای نمایش url به ضورت کامل استفاده میشه
    profile_image_uploaded = serializers.ImageField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = ProfileModel
        fields = ['profile_image', 'profile_image_uploaded']

    def get_profile_image(self, obj):
        '''
        باعث میشه عکس به این صورت نمایش داده بشه در خروجی
        http://localhost:8000/media/profiles_image/image.jpg
        '''
        if obj.profile_image:
            return self.context['request'].build_absolute_uri(obj.profile_image.url)
        return None

    def validate_profile_image_uploaded(self, value):
        if value:
            max_size = 5 * 1024 * 1024 #محدودیت اندازه فایل (5 مگابایت)
            if value.size > max_size:
                raise serializers.ValidationError({"iamge_size":"Image size should not exceed 5MB."})
            allowed_formats = ['image/jpg', 'image/jpeg', 'image/png', 'image/gif']
            if value.content_type not in allowed_formats:
                raise serializers.ValidationError({"image_format":"Only JPG, JPEG, PNG, and GIF formats are allowed."})
        return value


class ProfileUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'profile')
        extra_kwargs = {
            'username': {'read_only': True},
            'email': {'read_only': True},
        }

    def update(self, instance, validated_data):
        # جدا کردن داده‌های پروفایل
        profile_data = validated_data.pop('profile', {})
        profile = instance.profile  

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        # آپدیت فیلدهای User
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # آپدیت فیلدهای Profile
        profile = instance.profile
        profile_image_uploaded = profile_data.get('profile_image_uploaded')
        if profile_image_uploaded is not None:  # اگر None بود، تغییر نده (برای delete اگر نیاز داشتی، جدا هندل کن)
            profile.profile_image = profile_image_uploaded
        profile.save()

        return instance
    

class GetProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'profile')
        extra_kwargs = {
            'username': {'read_only': True},
            'email': {'read_only': True},
        }