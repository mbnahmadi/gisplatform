from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

class Usermanager(BaseUserManager):
    '''
    اگه مستقیم از create_user یا createsuperuser استفاده کنیم درین صورت این دستورات اعمال میشه و ربطی به پنل ادمین نداره
    '''
    def create_user(self, email, username, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password) # پسورد رو هش میکنه
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        if password is None:
            raise ValueError('Superuser must have a password.')
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email=email, username=username, password=password, **extra_fields)


class CustomUserModel(AbstractUser):
    email = models.EmailField(verbose_name=_('Email'), unique=True)
    is_email_verified = models.BooleanField(verbose_name=_('Email verified?'), default=False)

    is_2FA_enabled = models.BooleanField(verbose_name=_('2 FA enabled?'), default=False)
    mobile = PhoneNumberField(verbose_name=_('phone number'), unique=True, null=True, blank=True)
    pending_mobile = PhoneNumberField(null=True, blank=True)
    is_mobile_verified = models.BooleanField(_("phone number verified?"), default=False)



    objects = Usermanager()

    USERNAME_FIELD = 'username' # اینجا هر چی باشه باهمون میشه لاگین کرد توی ادمین
    REQUIRED_FIELDS = ['email']  # REQUIRED_FIELDS مشخص می‌کند که کدام فیلدها هنگام ایجاد سوپریوزر (از طریق createsuperuser) باید پر شوند.

    def __str__(self):
        return f'{self.email}'