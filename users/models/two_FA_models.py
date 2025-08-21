from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class TwoFAModels(models.Model):
    PURPOSE_CHOICES = (
        ('Verfy phone', 'verify_phone'),
        ('Login 2FA', 'Login_2FA')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE)
    mobile = PhoneNumberField(verbose_name=_('phone number'))
    is_used = models.BooleanField(default=False, verbose_name=_('is_used'))
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, verbose_name=_('purpose'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    attempts = models.IntegerField(default=0, null=False, verbose_name=_('attempts'))
    is_mobile_verified = models.BooleanField(_("phone number verified?"))

    
    class Meta:
        verbose_name = _('Two Factor Authenticate Mobiles')
        verbose_name_plural = _('Two Factor Authenticate Mobile')

    def __str__(self):
        return f"{self.user.username} - {self.user.email} - {self.mobile}"