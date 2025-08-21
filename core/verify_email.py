from rest_framework.exceptions import ValidationError
from users.models.email_code_models import EmailCodeModel
from users.models.two_FA_models import TwoFAModels
from django.db.models import F
from django.db import transaction
from django.conf import settings

def verify_user_email(user, code, purpose):
    """
    تلاش می‌کند آخرین OTP معتبر را قفل کند و بررسی نماید.
    اگر موفق باشد، OTP را مصرف می‌کند و رکورد otp را برمی‌گرداند.
    اگر ناموفق باشد ValidationError یا OTPCodeModel.DoesNotExist می‌رود بالا.
    error_message باید خارج ترنزاکشن انجام بشن چون اگه raise بدیم ترنس اکشن rollback میکنه
    """
    # باعث میشخ یا این تراکنش کامل انجام بشه یا اصلا انجام نشه
    with transaction.atomic():
        # می‌گیریم آخرین otp که هنوز مصرف نشده (و قفل می‌کنیم)
        # با select_for_update قفل میشه
        code_qs = EmailCodeModel.objects.select_for_update().filter(
            user=user,
            purpose=purpose,
            is_used=False
        ).order_by('-created_at')

        raw_code = code_qs.first() # اخرین کوئری بدست امده
        if not raw_code:
            error_message = "Invalid code or no code found."
        # بررسی انقضا
        elif raw_code.is_expired():
            error_message = "Code expired."

        # افزایش تعداد تلاش (atomic چون داخل تراکنش است)
        # با استفاده از F این افزایش مستقیم روی این فیلد اتفاق میوفته نه توی پایتون
        # raw_code.attempts = F('attempts') + 1
        # raw_code.save(update_fields=['attempts'])
        else:
            EmailCodeModel.objects.filter(pk=raw_code.pk).update(attempts=F('attempts') + 1)

            # refresh از DB تا مقدار واقعی attempts را داشته باشیم
            raw_code.refresh_from_db(fields=['attempts'])

            # اگر از حد مجاز بیشتر شده باشد
            max_attempts = getattr(settings, 'VERIFY_EMAIL_CODE_MAX_ATTEMPTS')
            #getattr(settings, 'VERIFY_EMAIL_CODE_MAX_ATTEMPTS', 3) # از ستینگ بیا VERIFY_EMAIL_CODE_MAX_ATTEMPTS رو بگیر اگه نداشت 3 بذار
            if raw_code.attempts > max_attempts:
                error_message = "Too many attempts. Please request a new code."

        # بررسی کد
            elif not raw_code.check_code(code):
                # کد اشتباه است ولی چون attempts افزایش یافته، تا رسیدن به حداکثر ادامه می‌یابد
                error_message = "Invalid code."

            else:
                raw_code.is_used = True
                raw_code.save(update_fields=['is_used'])  #update_fields فقط همین فیلد اپدیت میشه نه کل فیلد ها
    # حالا خارج از atomic، اگر error بود پرتاب کن (تغییرات commit شدن)
    if error_message:
        raise ValidationError(error_message)

    return raw_code


def verify_user_mobile_2FA(user, code, purpose):
    """
    تلاش می‌کند آخرین OTP معتبر را قفل کند و بررسی نماید.
    اگر موفق باشد، OTP را مصرف می‌کند و رکورد otp را برمی‌گرداند.
    اگر ناموفق باشد ValidationError یا OTPCodeModel.DoesNotExist می‌رود بالا.
    error_message باید خارج ترنزاکشن انجام بشن چون اگه raise بدیم ترنس اکشن rollback میکنه
    """
    # باعث میشخ یا این تراکنش کامل انجام بشه یا اصلا انجام نشه
    with transaction.atomic():
        # می‌گیریم آخرین otp که هنوز مصرف نشده (و قفل می‌کنیم)
        # با select_for_update قفل میشه
        code_qs = TwoFAModels.objects.select_for_update().filter(
            user=user,
            purpose=purpose,
            is_used=False
        ).order_by('-created_at')

        raw_code = code_qs.first() # اخرین کوئری بدست امده
        if not raw_code:
            error_message = "Invalid code or no code found."
        # بررسی انقضا
        elif raw_code.is_expired():
            error_message = "Code expired."

        else:
            EmailCodeModel.objects.filter(pk=raw_code.pk).update(attempts=F('attempts') + 1)

            # refresh از DB تا مقدار واقعی attempts را داشته باشیم
            raw_code.refresh_from_db(fields=['attempts'])

            # اگر از حد مجاز بیشتر شده باشد
            max_attempts = getattr(settings, 'VERIFY_CODE_MAX_ATTEMPTS')
            #getattr(settings, 'VERIFY_EMAIL_CODE_MAX_ATTEMPTS', 3) # از ستینگ بیا VERIFY_EMAIL_CODE_MAX_ATTEMPTS رو بگیر اگه نداشت 3 بذار
            if raw_code.attempts > max_attempts:
                error_message = "Too many attempts. Please request a new code."

        # بررسی کد
            elif not raw_code.check_code(code):
                # کد اشتباه است ولی چون attempts افزایش یافته، تا رسیدن به حداکثر ادامه می‌یابد
                error_message = "Invalid code."

            else:
                raw_code.is_used = True
                raw_code.save(update_fields=['is_used'])  #update_fields فقط همین فیلد اپدیت میشه نه کل فیلد ها
    # حالا خارج از atomic، اگر error بود پرتاب کن (تغییرات commit شدن)
    if error_message:
        raise ValidationError(error_message)

    return raw_code

