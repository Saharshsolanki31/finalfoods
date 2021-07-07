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

from restaurant import views

urlpatterns = [
    path('register',views.register,name="restaurant_registraion"),
    path('otp_verification',views.verify_otp,name="restaurant_otp_verification"),

    path('login',views.login,name="restaurant_login"),
    path('account/recovery/password',views.reset_password,name="restaurant_reset_password"),
    path('account/recovery/password/verify/otp',views.varify_reset_password_otp,name="restaurant_reset_password_verify_otp"),
    path('account/recovery/password/resend/otp',views.resend_reset_password_otp,name="restaurant_reset_password_resend_otp"),
    path('account/register/resend/otp',views.resend_reg_otp,name="restaurant_register_resend_otp"),
    path('home',views.restaurant_home,name="restaurant_home"),
    path('menu',views.menu,name="restaurant_menu"),
    path('menu/add/dish_category',views.add_dish_category,name='add_dish_category'),
    path('menu/add/food_item',views.add_food_item,name="add_food_item"),
    path('menu/update/menu_item/<id>',views.edit_menu_item,name="edit_menu_item"),
    path('menu/update/menu_item',views.update_menu_item,name="update_menu_item"),
    path('menu/delete/menu_item/<id>',views.delete_menu_item,name="delete_menu_item"),
    path('menu/update/food_item/<id>',views.edit_food_item,name="edit_food_item"),
    path('menu/update/food_item',views.update_food_item,name="update_food_item"),
    path('menu/delete/food_item/<id>',views.delete_food_item,name="delete_food_item"),
    # path('menu/add/food',views.menu,name="restaurant_menu"),
    path('table',views.table,name="table"),
    path('orders',views.orders,name="orders"),
    path('logout',views.logout,name="logout"),
    path('make_new_order', views.make_new_order, name="make_new_order"),
    path('complete_order', views.complete_order, name="complete_order"),
    path('pending_order', views.pending_order, name="pending_order"),
    path('save_order', views.save_order, name="save_order"),
path('on_order/<id>', views.on_order, name="on_order"),
path('update_item_quantity/<id>', views.update_item_quantity, name="update_item_quantity"),
path('cancel_item/<id>', views.cancel_item, name="cancel_item"),
path('confirm_order', views.confirm_order, name="confirm_order"),
path('cancel_order_status/<id>', views.cancel_order_status, name="cancel_order_status"),
path('complete_order_statusv/<id>', views.complete_order_status, name="complete_order_status"),
path('profile/', views.profile, name="profile"),
path('update_profile/', views.update_profile, name="update_profile"),
path('tables_booking/', views.tables_booking, name="tables_booking"),
path('confirm_table_booking/<id>', views.confirm_table_booking, name="confirm_table_booking"),
path('cancel_table_booking/<id>', views.cancel_table_booking, name="cancel_table_booking"),

]
