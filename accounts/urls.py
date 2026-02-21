from django.urls import path
from . import views

urlpatterns = [

    # ================= AUTH =================
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # ================= REGISTER FLOW =================
    path("register/", views.register, name="register"),
    path("verify-email/", views.verify_email, name="verify_email"),

    # ================= PASSWORD RESET FLOW =================
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("verify-reset-otp/", views.verify_reset_otp, name="verify_reset_otp"),
    path("reset-password/", views.reset_password, name="reset_password"),
      path("verify-otp/", views.verify_otp, name="verify_otp"),
      path("resend-otp/", views.resend_email_otp, name="resend_email_otp"),
            path("set_password/", views.set_password, name="set_password"),



]