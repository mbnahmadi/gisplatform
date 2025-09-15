import random
from users.models.email_code_models import EmailCodeModel, ResetPasswordTokenModel
from users.models.two_FA_models import TwoFAModels
from django.db import transaction
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from notifications.tasks import send_email_task, send_reset_password_email_code
import logging


def send_code_to_email(user, purpose):
    '''
    فقط کد ارسال میکنه برای تایید ایمیل
    '''
    #  بررسی آخرین زمان ارسال
    # کاربر هر 2 دقیقه یکبار میتونه درخواست بده
    # CODE_RESEND_INTERVAL_SECONDS همین باعث میشه کد را هر 2 دقیقه یکبار بتونه درخواست بده
    last_code = EmailCodeModel.objects.filter(user=user, purpose=purpose).order_by('-created_at').first()
    # print('last_code', last_code)
    if last_code and last_code.created_at > timezone.now() - timedelta(seconds=settings.CODE_RESEND_INTERVAL_SECONDS):
        remaining_second = (last_code.created_at + timedelta(seconds=settings.CODE_RESEND_INTERVAL_SECONDS) - timezone.now()).seconds
        raise ValidationError(f'Please wait {remaining_second} second before requesting another code to send.')

    raw_code = str(random.randint(100000, 999999))
    EmailCodeModel.objects.create(user=user, code=raw_code, purpose=purpose) # کد رو میسازه و توی دیتابیس ذخیره میکنه

    # raise Exception("Simulated email failure")

    subject = "Here is your code!"
    if purpose == 'change_email':
        message = f"Verify your email to change old email:\n {raw_code}"
    else:
        message = f"continue signing up by entering the code below:\n {raw_code}"
    try:
        # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email]) # کد رو راسال میکنه به کاربر
        send_email_task.delay(subject, message, user.email)
    except Exception as e:
        raise ValidationError(f"Failed to send email: {str(e)}") 

    return True



def send_otp_code(user, purpose):
    '''
    ابتدا کد رو در دیتابیس میسازه و سپس ارسال میکنه برای تایید موبایل و همچنین لاگین برای احراز هویت دو مرحله ای
    '''
    last_code = TwoFAModels.objects.filter(user=user, purpose=purpose).order_by('-created_at').first()
    if last_code and last_code.created_at > timezone.now() - timedelta(seconds=settings.CODE_RESEND_INTERVAL_SECONDS):
        remaining_second = (last_code.created_at + timedelta(seconds=settings.CODE_RESEND_INTERVAL_SECONDS) - timezone.now()).seconds
        raise ValidationError(f'Please wait {remaining_second} second before requesting another code to send.')

    raw_code = str(random.randint(100000, 999999))
    TwoFAModels.objects.create(user=user, code=raw_code, purpose=purpose)
    try:
        print(f'[Debug] OTP send to {user.mobile}: {raw_code} - {purpose}')
    except Exception as e:
        raise ValidationError(f"Failed to send sms: {str(e)}") 


logger = logging.getLogger(__name__)
def create_reset_password_link(user, request=None):
    last_token = ResetPasswordTokenModel.objects.filter(user=user).order_by('-created_at').first()
    if last_token and last_token.created_at > timezone.now() - timedelta(seconds=settings.CODE_RESEND_INTERVAL_SECONDS):
        remaining_second = (last_token.created_at + timedelta(seconds=settings.CODE_RESEND_INTERVAL_SECONDS) - timezone.now()).seconds
        raise ValidationError(f"Please wait {remaining_second} seconds before requesting another reset password link to send.")
    # create token
    token_obj = ResetPasswordTokenModel.objects.create(user=user)

    # FRONTEND_BASE_URL = "https://app.example.com"
    # FRONTEND_RESET_PATH = "/auth/reset-password"
    base = getattr(settings, "FRONTEND_BASE_URL", None)
    path = getattr(settings, "FRONTEND_RESET_PATH", "/reset-password/")
    if base:
        reset_link = f"{base.rstrip('/')}{path}?token={token_obj.token}"
    else:
        if not request:
            raise ValidationError("FRONTEND_BASE_URL is not set and request is required for fallback.")
        reset_link = request.build_absolute_uri(
            reverse("password-reset-confirm") + f"?token={token_obj.token}"
        )

    def send_email_task():
        try:
            send_reset_password_email_code.delay(user.email, reset_link, user.username)
        except Exception as e:
            logger.error(f"Failed to send reset password email to {user.email}: {e}")

    transaction.on_commit(send_email_task)
    return reset_link

    