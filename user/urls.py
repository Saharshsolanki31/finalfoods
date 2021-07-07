"""food URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from user import views

urlpatterns = [
    path('register',views.register,name="user_registraion"),
    path('otp_verification',views.verify_otp,name="otp_verification"),
    path('login',views.login,name="user_login"),
    path('account/recovery/password', views.reset_password, name="user_reset_password"),
    path('account/recovery/password/verify/otp', views.varify_reset_password_otp,name="user_reset_password_verify_otp"),
    path('account/recovery/password/resend/otp', views.resend_reset_password_otp,name="user_reset_password_resend_otp"),
    path('account/register/resend/otp', views.resend_reg_otp, name="user_register_resend_otp"),
    path('home',views.home,name="user_home"),
    path('user_profile', views.user_profile, name="user_profile"),
    path('update_user_profile', views.update_user_profile, name="update_user_profile"),
    path('book_table/<id>', views.book_table, name="book_table"),
    path('cancel_booking/<id>', views.cancel_booking, name="cancel_booking"),

    path('logout',views.logout,name="user_logout"),
]
