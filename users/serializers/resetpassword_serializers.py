from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from core.verify_code import verify_user_mobile_2FA_code
from users.models.profile_models import ProfileModel


