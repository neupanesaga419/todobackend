from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


@shared_task
def send_otp_email(email, otp, first_name, last_name):

    subject = "Email Verification OTP"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    # Render the HTML template with context
    html_message = render_to_string(
        "verify_otp.html", {"otp_code": otp, "user_name": f"{first_name} {last_name}"}
    )

    send_mail(subject, "", from_email, recipient_list, html_message=html_message)


@shared_task
def send_welcome_email(email, first_name, last_name):
    subject = "Welcome to JWT Todo"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    # Render the HTML template with context
    html_message = render_to_string(
        "welcome_email.html", {"user_name": f"{first_name} {last_name}"}
    )

    send_mail(subject, "", from_email, recipient_list, html_message=html_message)


@shared_task
def send_reset_password_otp(email, otp, first_name, last_name):

    subject = "Reset Password OTP"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    # Render the HTML template with context
    html_message = render_to_string(
        "reset_password.html",
        {"otp_code": otp, "user_name": f"{first_name} {last_name}"},
    )

    send_mail(subject, "", from_email, recipient_list, html_message=html_message)


@shared_task
def send_success_email(email, first_name, last_name):
    subject = "Password Reset Successful"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    # Render the HTML template with context
    html_message = render_to_string(
        "password_reset_success.html",
        {"user_name": f"{first_name} {last_name}"},
    )

    send_mail(subject, "", from_email, recipient_list, html_message=html_message)
