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
        