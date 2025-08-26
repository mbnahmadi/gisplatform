from celery import shared_task
import time

@shared_task
def send_test_email(user_email):
    # شبیه‌سازی ارسال ایمیل
    print(f"Sending email to {user_email}...")
    time.sleep(5)  # شبیه‌سازی زمان ارسال
    print(f"Email sent to {user_email}!")
    return f"Email sent to {user_email}"


@shared_task
def add(x, y):
    return x + y