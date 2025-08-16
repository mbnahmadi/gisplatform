from django.contrib import admin
from .models import CustomUserModel
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.utils.translation import gettext_lazy as _

# Register your models here.

class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ('email', 'username', 'is_email_verified', 'is_2FA_enabled')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'is_email_verified', 'is_2FA_enabled')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # برای اد کردن یوزر
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'confirm_password')}#
        ),
    )

    list_display = ('username', 'email', 'is_superuser')
    ordering = ('date_joined',)


admin.site.register(CustomUserModel, CustomUserAdmin)
    
