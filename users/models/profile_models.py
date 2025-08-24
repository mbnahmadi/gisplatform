from django.db import models
from django.conf import settings
from core.media_path import user_media_image_path
from django.utils.translation import gettext_lazy as _


class ProfileModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(verbose_name=_('Profile Image'), upload_to=f'profile_images/{user_media_image_path}', null=True, blank=True)


    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return f"{self.user.username} - {self.user.first_name} - {self.user.last_name}"


