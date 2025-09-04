import uuid
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import gettext_lazy as _


class EmailCodeModel(models.Model):
    PURPOSE_CHOICES = (
        ('verify_email', 'Verify Email'),
        ('reset_password', 'Reset Password'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('User'))
    code = models.CharField(verbose_name=_('Code'), max_length=128)
    is_used = models.BooleanField(default=False, verbose_name=_('is_used'))
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, verbose_name=_('purpose'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    attempts = models.IntegerField(default=0, null=False, verbose_name=_('attempts')) # تعداد تلاش ها اگر بیشتر از 3 بار اشتباه وارد بشه دباره باید درخواست بده

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
        verbose_name = _('Email code verification')
        verbose_name_plural = _('Email codes verification')

        indexes = [
            models.Index(fields=['user', 'purpose', 'is_used'])
        ]

    def __str__(self):
        return f"{self.user.username} - {self.user.email}"



class ResetPasswordTokenModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('User'), related_name='reset_password_token')
    token = models.UUIDField(verbose_name=_('token'), default=uuid.uuid4, editable=False, unique=True)
    is_used = models.BooleanField(verbose_name=_('is_used'), default=False)
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)

    def is_expired(self) -> bool:
        expiry_time = self.created_at + timedelta(seconds=settings.VERIFICATION_TOKEN_EXPIRE_SECONDS)
        return timezone.now() > expiry_time

    def mark_as_used(self):
        self.is_used = True
        self.save(update_fields=['is_used'])

    class Meta:
        indexes = [
            models.Index(fields=["user", "is_used", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.user_id} - {self.token}"