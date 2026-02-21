import random
import hashlib
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import OTP


OTP_EXPIRY_MINUTES = 5


def generate_otp():
    return str(random.SystemRandom().randint(100000, 999999))


def hash_otp(otp):
    return hashlib.sha256(otp.encode()).hexdigest()


def send_email_otp(user):
    otp = generate_otp()
    otp_hash = hash_otp(otp)

    # Delete old OTPs
    OTP.objects.filter(user=user).delete()

    OTP.objects.create(
        user=user,
        otp_hash=otp_hash
    )

    send_mail(
        subject="Email Verification OTP",
        message=f"""
Hello {user.username},

Your OTP is: {otp}

It is valid for {OTP_EXPIRY_MINUTES} minutes.
Do not share it with anyone.
""",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )


def verify_email_otp(user, entered_otp):
    try:
        otp_obj = OTP.objects.get(user=user)
    except OTP.DoesNotExist:
        return False, "No OTP found"

    # Check expiry
    if otp_obj.is_expired():
        otp_obj.delete()
        return False, "OTP expired"

    entered_hash = hash_otp(entered_otp)

    if entered_hash != otp_obj.otp_hash:
        otp_obj.attempts += 1
        otp_obj.save()

        if otp_obj.attempts >= 3:
            otp_obj.delete()
            return False, "Too many attempts"

        return False, "Invalid OTP"

    # Success
    user.is_email_verified = True
    user.save()
    otp_obj.delete()

    return True, "Verified successfully"