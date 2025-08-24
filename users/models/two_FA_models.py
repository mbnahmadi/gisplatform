from datetime import timedelta
from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TwoFAModels(models.Model):
    PURPOSE_CHOICES = (
        ('verify_phone', 'Verfy phone'),
        ('Login_2FA', 'Login 2FA')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE, related_name='twofa')
    code = models.CharField(verbose_name=_('Code'), max_length=128)
    is_used = models.BooleanField(default=False, verbose_name=_('is_used'))
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, verbose_name=_('purpose'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    attempts = models.IntegerField(default=0, null=False, verbose_name=_('attempts'))

    
    def save(self, *args, **kwargs):
        if not self.pk: # برای اولین بار فقط هش کن
            self.code = make_password(self.code)
        super().save(*args, **kwargs)


    def check_code(self, raw_code):
        return check_password(raw_code, self.code) # مقایسه کد ورودی و کدی که در دیتابیس وجود داره

    
    def is_expired(self):
        expiry_time = self.created_at + timedelta(seconds=settings.VERIFICATION_CODE_EXPIRE_SECONDS)
        return timezone.now() > expiry_time # expires after 5 min




    class Meta:
        verbose_name = _('Two Factor Authenticate Mobiles')
        verbose_name_plural = _('Two Factor Authenticate Mobile')
        indexes = [
            models.Index(fields=['user', 'purpose', 'is_used'])
        ]



    def __str__(self):
        return f"{self.user.username} - {self.user.mobile}"