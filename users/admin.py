from django.contrib import admin
from django.contrib.auth.models import User

from .models import CustomUserModel, EmailCodeModel, TwoFAModels, ProfileModel, ResetPasswordTokenModel
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # فقط برای خود یوزر تعریف شده
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.utils.translation import gettext_lazy as _

# Register your models here.
class ProfileInlineAdmin(admin.StackedInline):
    model = ProfileModel
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'




class CustomUserAdmin(BaseUserAdmin):
    inlines = [ProfileInlineAdmin]


    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ('email', 'username', 'is_email_verified', 'is_2FA_enabled')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('2 factor authenticate info'), {'fields': ('is_2FA_enabled', 'mobile', 'is_mobile_verified')}),
        (_('Permissions'), {'fields': ('is_email_verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # برای اد کردن یوزر
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'confirm_password')}#
        ),
    )

    list_select_related = ('profile',)
    def get_profile_image(self, instance):
        return instance.profile.profile_image if instance.profile else None
    get_profile_image.short_description = 'Profile Image'

    # def get_first_name(self, obj):
    #     return obj.user.first_name
    # get_first_name.short_description = 'first name'

    # def get_profile_image(self, instance):
    #     return instance.profile.profile_image if instance.profile else None
    # get_profile_image.short_description = 'Profile Image'

    # list_display = ('username', 'email', 'is_superuser')
    ordering = ('date_joined',)


admin.site.register(CustomUserModel, CustomUserAdmin)

admin.site.register(EmailCodeModel)
admin.site.register(TwoFAModels)
admin.site.register(ResetPasswordTokenModel)



# class ProfileAdmin(admin.ModelAdmin):

    # list_display = ('get_username', 'get_email', 'get_first_name', 'get_last_name', 'profile_image')

    # def get_username(self, obj):
    #     return obj.user.username
    # get_username.admin_order_field = 'user__username'
    # get_username.short_description = 'Username'

    # def get_email(self, obj):
    #     return obj.user.email
    # get_email.admin_order_field = 'user__email'
    # get_email.short_description = 'Email'

    # def get_first_name(self, obj):
    #     return obj.user.first_name
    # get_first_name.short_description = 'First Name'

    # def get_last_name(self, obj):
    #     return obj.user.last_name
    # get_last_name.short_description = 'Last Name'


# admin.site.register(ProfileModel, ProfileAdmin)
# , 'email', 'first_name', 'last_name'