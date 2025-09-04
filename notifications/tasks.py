from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger('notification')


@shared_task
def send_email_task(subject, message, to_email):
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])
        logger.info(f"email send to {to_email}")

    except Exception as e:
        logger.error(f"failed to send email to {to_email}: {e}", exc_info=True)
        

@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def send_reset_password_email_code(self, to_email, reset_link, user_name):
    subject = "Reset your password"
    message = f"Dear {user_name},\n\nClick the link below to reset your password:\n{reset_link}\n\nThis link will expire in {settings.PASSWORD_RESET_TOKEN_TTL_MINUTES} minutes.\n\nIf you didn't request this, please ignore this email.\n\nBest regards"
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email], fail_silently=False)
    except Exception as exc:
        logger.error(f"Failed to send reset password email to {to_email}: {exc}")
        # تلاش دوباره برای ارسال دوباره ایمیل 
        # در کل max_retries بار تلاش میکنه با تاخیر default_retry_delay
        raise self.retry(exc=exc) 