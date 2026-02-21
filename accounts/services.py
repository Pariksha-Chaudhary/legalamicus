# accounts/services.py

import logging
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client

logger = logging.getLogger(__name__)


# ================= EMAIL SERVICE =================

def send_email_otp(email, otp):
    """
    Production-safe email sender.
    Will NEVER crash your website.
    """

    try:
        # If running locally without SMTP configured
        if not settings.EMAIL_HOST_USER:
            print(f"[DEV MODE] OTP for {email}: {otp}")
            return True

        send_mail(
            subject="Your OTP Verification",
            message=f"Your OTP is {otp}. It expires in 5 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return True

    except Exception as e:
        logger.error(f"Email sending failed: {e}")
        print(f"[EMAIL FAILED] OTP for {email}: {otp}")
        return False


# ================= SMS SERVICE =================

def send_sms_otp(phone, otp):
    """
    Production-safe SMS sender.
    Will NOT crash if Twilio fails.
    """

    try:
        if not settings.TWILIO_ACCOUNT_SID:
            print(f"[DEV MODE] SMS OTP for {phone}: {otp}")
            return True

        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

        client.messages.create(
            body=f"Your OTP is {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone
        )

        return True

    except Exception as e:
        logger.error(f"SMS sending failed: {e}")
        print(f"[SMS FAILED] OTP for {phone}: {otp}")
        return False
