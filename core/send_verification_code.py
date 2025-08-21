import random
from users.models.email_code_models import EmailCodeModel
from users.models.two_FA_models import TwoFAModels
# from users.models.
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone
from django.conf import settings


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
        raise ValidationError("Please wait before requesting another code to send.")

    raw_code = str(random.randint(100000, 999999))
    EmailCodeModel.objects.create(user=user, code=raw_code, purpose=purpose) # کد رو میسازه و توی دیتابیس ذخیره میکنه

    # raise Exception("Simulated email failure")

    subject = "Here is your code!"
    message = f"continue signing up by entering the code below:\n {raw_code}"
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email]) # کد رو راسال میکنه به کاربر
    except Exception as e:
        raise ValidationError(f"Failed to send email: {str(e)}") 

    return True



def send_otp_code(user, purpose):
    '''
    فقط کد ارسال میکنه برای تایید موبایل و همچنین لاگین برای احراز هویت دو مرحله ای
    '''
    last_code = TwoFAModels.objects.filter(user=user, purpose=purpose).order_by('-created_at').first()
    if last_code and last_code.created_at > timezone.now() - timedelta(seconds=settings.CODE_RESEND_INTERVAL_SECONDS):
        raise ValidationError('Please wait before requesting another code to send.')

    raw_code = str(random.randint(100000, 99999))
    TwoFAModels.objects.create(user=user, code=raw_code, purpose=purpose)

    print(f'[Debug] OTP send to {user.mobile}: {raw_code}')