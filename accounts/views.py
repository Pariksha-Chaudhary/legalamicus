from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from .utils import send_email_otp, verify_email_otp
import re
from datetime import date

User = get_user_model()


# ================= REGISTER =================
import uuid

def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        role = request.POST.get("role")

        if not email:
            messages.error(request, "Email is required")
            return redirect("register")

        if not phone:
            messages.error(request, "Phone number is required")
            return redirect("register")

        # Check email uniqueness
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        # ✅ ADD THIS (Phone check)
        if User.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already registered")
            return redirect("register")

        username = email
        temp_password = str(uuid.uuid4())

        user = User.objects.create_user(
            username=username,
            email=email,
            password=temp_password,
            phone=phone,
            role=role,
            is_active=True,
        )

        send_email_otp(user)
        request.session["verify_user_id"] = user.id

        return redirect("/accounts/verify-email")

    return render(request, "accounts/register.html")
    # ================= VERIFY EMAIL =================
def verify_email(request):
    user_id = request.session.get("verify_user_id")

    if not user_id:
        return redirect("register")

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        otp = request.POST.get("otp")

        success, message = verify_email_otp(user, otp)

        if success:
            request.session["otp_verified_user"] = user.id
            return redirect("set_password")

        return render(request, "accounts/verify_email.html", {"error": message})

    return render(request, "accounts/verify_email.html")


# ================= LOGIN =================

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            if not user.is_email_verified:
                messages.error(request, "Please verify your email first")
                return redirect("login")

            login(request, user)
            return redirect("/")

        messages.error(request, "Invalid credentials")

    return render(request, "accounts/login.html")


# ================= FORGOT PASSWORD =================

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User not found")
            return redirect("forgot_password")

        send_email_otp(user)
        request.session["reset_user_id"] = user.id

        return redirect("verify_reset_otp")

    return render(request, "accounts/forgot_password.html")


# ================= VERIFY RESET OTP =================

def verify_reset_otp(request):
    user_id = request.session.get("reset_user_id")

    if not user_id:
        return redirect("forgot_password")

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        otp = request.POST.get("otp")

        success, message = verify_email_otp(user, otp)

        if success:
            request.session["otp_verified"] = True
            return redirect("reset_password")

        return render(request, "accounts/verify_reset_otp.html", {"error": message})

    return render(request, "accounts/verify_reset_otp.html")


# ================= RESET PASSWORD =================

def reset_password(request):
    if not request.session.get("otp_verified"):
        return redirect("forgot_password")

    user_id = request.session.get("reset_user_id")

    if not user_id:
        return redirect("forgot_password")

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("reset_password")

        user.set_password(password1)
        user.save()

        request.session.flush()
        return redirect("login")

    return render(request, "accounts/reset_password.html")


# ================= LOGOUT =================

def logout_view(request):
    logout(request)
    return redirect("/")

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        session_otp = request.session.get("otp")

        if entered_otp == session_otp:
            request.user.is_active = True
            request.user.save()

            del request.session["otp"]

            return redirect("home")  # change to your home url

        else:
            messages.error(request, "Invalid OTP")

    return render(request, "accounts/verify_otp.html")

def resend_email_otp(request):
    user_id = request.session.get("verify_user_id")

    if not user_id:
        return redirect("register")

    user = User.objects.get(id=user_id)
    send_email_otp(user)

    messages.success(request, "OTP has been resent to your email.")
    return redirect("verify_email")


def set_password(request):
    user_id = request.session.get("otp_verified_user")

    if not user_id:
        return redirect("register")

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        username = request.POST.get("username")
        dob = request.POST.get("dob")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Username validation
        if User.objects.filter(username=username).exclude(id=user.id).exists():
            messages.error(request, "Username already taken")
            return redirect("set_password")

        # DOB validation (18+)
        dob_obj = date.fromisoformat(dob)
        age = (date.today() - dob_obj).days // 365
        if age < 18:
            messages.error(request, "You must be at least 18 years old")
            return redirect("set_password")

        # Password match
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("set_password")

        # Password strength checks
        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect("set_password")

        if not re.search(r"[A-Z]", password1):
            messages.error(request, "Password must include one uppercase letter")
            return redirect("set_password")

        if not re.search(r"[0-9]", password1):
            messages.error(request, "Password must include one number")
            return redirect("set_password")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password1):
            messages.error(request, "Password must include one special character")
            return redirect("set_password")

        # Save user
        user.username = username
        user.dob = dob
        user.set_password(password1)
        user.is_email_verified = True
        user.save()

        login(request, user)
        request.session.flush()

        return redirect("/")

    return render(request, "accounts/set_password.html")