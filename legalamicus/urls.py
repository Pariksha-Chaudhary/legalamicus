from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('lawyers/', include('lawyers.urls')),
    path('', include('consultations.urls')),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path("practice/", include("practice.urls")),
       # 🔥 Password reset URLs
    path('password-reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
     path("chaining/", include("smart_selects.urls")),
    
]
