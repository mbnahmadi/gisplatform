from rest_framework.exceptions import ValidationError
from users.models.email_code_models import EmailCodeModel
from django.db.models import F
from django.db import transaction
from django.conf import settings

def verify_user_email(user, code, purpose):
    """
    تلاش می‌کند آخرین OTP معتبر را قفل کند و بررسی نماید.
    اگر موفق باشد، OTP را مصرف می‌کند و رکورد otp را برمی‌گرداند.
    اگر ناموفق باشد ValidationError یا OTPCodeModel.DoesNotExist می‌رود بالا.
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

        code = code_qs.first()
        if not code:
            raise ValidationError("Invalid code or no code found.")

        # بررسی انقضا
        if code.is_expired():
            raise ValidationError("Code expired.")

        # افزایش تعداد تلاش (atomic چون داخل تراکنش است)
        # با استفاده از F این افزایش مستقیم روی این فیلد اتفاق میوفته نه توی پایتون
        code.attempts = F('attempts') + 1
        code.save(update_fields=['attempts'])
        # refresh از DB تا مقدار واقعی attempts را داشته باشیم
        code.refresh_from_db()

        # اگر از حد مجاز بیشتر شده باشد
        max_attempts = getattr(settings, 'OTP_MAX_ATTEMPTS')
        #getattr(settings, 'OTP_MAX_ATTEMPTS', 3) # از ستینگ بیا OTP_MAX_ATTEMPTS رو بگیر اگه نداشت 3 بذار
        if code.attempts > max_attempts:
            raise ValidationError("Too many attempts. Please request a new code.")

        # بررسی کد
        if not code.check_code(code):
            # کد اشتباه است ولی چون attempts افزایش یافته، تا رسیدن به حداکثر ادامه می‌یابد
            raise ValidationError("Invalid code.")

        
        code.is_used = True
        code.save(update_fields=['is_used'])  #update_fields فقط همین فیلد اپدیت میشه نه کل فیلد ها

        return code