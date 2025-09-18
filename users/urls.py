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
    LogOutView,
    ChangePasswordView,
    ChangeUsernameView,
    RequestEnable2FAView,
    VerifyEnable2FAView,
    ProfileView,
    ResetPasswordRequestView,
    ResetPasswordConfirmView,
    RequestDisable2FAView,
    ConfirmDisable2FAView,
    RequestChangeEmailView,
    ConfirmChangeEmailView,
    RequestChangeNumber2FAView,
    ConfirmOldChangeNumber2FAView,
    ConfirmNewChangeNumber2FAView
)
from users.views.account_view import ConfirmNewChangeNumber2FAView, ConfirmOldChangeNumber2FAView

urlpatterns = [
    # register
    path('register/', RegisterUserView.as_view(), name='register'),
    path('register/verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('register/resend-verification-code/', ResendVerificationCodeView.as_view(), name='resend-verification-code'),

    # login
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login-refresh'),
    path('login/verify-OTP-2fa/', VerifyLoginOTPCode2FAView.as_view(), name='verify-OTP-2fa'),

    # account
    path('account/logout/', LogOutView.as_view(), name='logout'),
    path('account/changepassword/', ChangePasswordView.as_view(), name='changepassword'),
    path('account/changeusername/', ChangeUsernameView.as_view(), name='changeusername'),
    path('account/changeemail/request/', RequestChangeEmailView.as_view(), name='changeemail-request'),
    path('account/changeemail/confirm/', ConfirmChangeEmailView.as_view(), name='changeemail-confirm'),
    path('account/twofa/enable/request/', RequestEnable2FAView.as_view(), name='enabletwofa-request'),
    path('account/twofa/enable/verfy/', VerifyEnable2FAView.as_view(), name='enabletwofa-verfy'),
    path('account/twofa/disable/request/', RequestDisable2FAView.as_view(), name='disabletwofa-request'),
    path('account/twofa/disable/confirm/', ConfirmDisable2FAView.as_view(), name='disabletwofa-confirm'),

    path('account/twofa/changenumber/request/', RequestChangeNumber2FAView.as_view(), name='changenumber-request'),
    path('account/twofa/changenumber/confirm/oldnumber/', ConfirmOldChangeNumber2FAView.as_view(), name='changenumber-confirm-oldnumber'),
    path('account/twofa/changenumber/confirm/newnumber/', ConfirmNewChangeNumber2FAView.as_view(), name='changenumber-confirm-newnumber'),
    # path('account/changenumber/request/', RequestEnable2FAView.as_view(), name='enabletwofa-request'),

    # profile
    path('prifile/', ProfileView.as_view(), name='profile'),
    
    #reset-password
    path('reset-password/request/', ResetPasswordRequestView.as_view(), name='reset-password-request'),
    path('reset-password/confirm/', ResetPasswordConfirmView.as_view(), name='reset-password-confirm'),

]
