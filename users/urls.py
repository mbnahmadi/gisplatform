"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import (
    RegisterUserView,
    VerifyEmailView,
    ResendVerificationCodeView,
    LoginView,
    VerifyLoginOTPCode2FAView,
    LogOutView
)

urlpatterns = [
    # register
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification-code/', ResendVerificationCodeView.as_view(), name='resend-verification-code'),

    # login
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login-refresh'),
    path('verify-OTP-2fa/', VerifyLoginOTPCode2FAView.as_view(), name='verify-OTP-2fa'),

    # account
    path('logout/', LogOutView.as_view(), name='logout'),

]
