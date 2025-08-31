import os
import logging
import logging.handlers
from django.conf import settings


LOG_FORMAT = '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s'

def _get_handlers(log_filename: str):
    """بر اساس نام فایل هندلر بسازه"""
    formatter = logging.Formatter(LOG_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=settings.BASE_DIR / f"logs/{log_filename}",        
        when="midnight",
        backupCount=7,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    return [console_handler, file_handler]


def setup_loggers():
    """
    برای هر اپ یک لاگر جدا می‌سازه
    """

    # --- users logger ---
    users_logger = logging.getLogger("users")
    users_logger.setLevel(logging.DEBUG)
    for handler in _get_handlers("users.log"):
        users_logger.addHandler(handler)

    # --- notification logger ---
    notif_logger = logging.getLogger("notification")
    notif_logger.setLevel(logging.DEBUG)
    for handler in _get_handlers("notification.log"):
        notif_logger.addHandler(handler)

    # --- core logger ---
    core_logger = logging.getLogger("core")
    core_logger.setLevel(logging.DEBUG)
    for handler in _get_handlers("core.log"):
        core_logger.addHandler(handler)

    # --- ایمیل فقط برای error های کل پروژه ---
    mail_handler = logging.handlers.SMTPHandler(
        mailhost=("smtp.gmail.com", 587),
        fromaddr=settings.DEFAULT_FROM_EMAIL,
        toaddrs=["admin@example.com"],   
        subject="GIS App Error",
        credentials=(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD),
        secure=()
    )
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    root_logger = logging.getLogger("config")
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(mail_handler)

    return {
        "users": users_logger,
        "notification": notif_logger,
        "core": core_logger,
        "config": root_logger
    }



# def setup_logger():
#     # formatter
#     formatter = logging.Formatter(LOG_FORMAT)

#     # console handler
#     console_handler = logging.StreamHandler()
#     console_handler.setFormatter(formatter)

#     # file handler (هر روز فایل جدید بسازه)
#     file_handler = logging.handlers.TimedRotatingFileHandler(
#         filename=settings.BASE_DIR / "logs/app.log",
#         when="midnight",
#         backupCount=7,
#         encoding="utf-8"
#     )
#     file_handler.setFormatter(formatter)


#     # email handler (برای error ها ایمیل بفرسته)
#     mail_handler = logging.handlers.SMTPHandler(
#         mailhost=("smtp.gmail.com", 587),
#         fromaddr=settings.DEFAULT_FROM_EMAIL,
#         toaddrs=["admin@example.com"],   
#         subject="GIS App Error",
#         credentials=(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD),
#         secure=()
#     )
#     mail_handler.setLevel(logging.ERROR)
#     mail_handler.setFormatter(formatter)


#     # root logger
#     logger = logging.getLogger("config")
#     logger.setLevel(logging.DEBUG)   # می‌تونی بگذاری INFO توی پرووداکشن
#     logger.addHandler(console_handler)
#     logger.addHandler(file_handler)
#     logger.addHandler(mail_handler)

#     return logger