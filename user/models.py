from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

# Model For User Data
from restaurant.models import food_item


class user(models.Model):
    email = models.CharField(max_length=250)
    phone = models.CharField(max_length=250,null=True)
    password = models.CharField(max_length=250)
    def __str__(self):
        return self.email



class address(models.Model):
    name = models.CharField(max_length=250)
    mobile_number = models.CharField(max_length=250)
    alternate_mobile_number = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    landmark = models.CharField(max_length=250,null=True,blank=True)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    pincode = models.CharField(max_length=250)
    latitude = models.CharField(max_length=250)
    longitude = models.CharField(max_length=250)
    user_id = models.ForeignKey(user,on_delete=models.CASCADE)
    def __str__(self):
        return self.mobile_number



class cart(models.Model):
    user_email = models.CharField(max_length=500)
    food_quantity = models.CharField(max_length=500,default='1')
    food_total_price = models.CharField(max_length=500,default='0')
    food_id = models.ForeignKey(food_item,on_delete=models.CASCADE)
    def __str__(self):
        return self.user_email


class user_order_id(models.Model):
    order_id = models.CharField(max_length=500)
    order_type = models.CharField(max_length=500)
    status = models.CharField(max_length=500,default="pending")
    user_id = models.ForeignKey(user,on_delete=models.CASCADE)
    pickup_time = models.CharField(max_length=500,blank=True,null=True)
    address_id = models.ForeignKey(address,on_delete=models.CASCADE,blank=True,null=True)
    order_id_created_at = models.DateTimeField(auto_now_add=True)
    payment_type =models.CharField(max_length=500)
    def __str__(self):
        return self.order_id


class user_order_item(models.Model):
    user_email = models.ForeignKey(user,on_delete=models.CASCADE)
    user_order_id = models.ForeignKey(user_order_id, on_delete=models.CASCADE)
    food_quantity = models.CharField(max_length=500,default='1')
    food_total_price = models.CharField(max_length=500,default='0')
    food_id = models.ForeignKey(food_item,on_delete=models.CASCADE)
    def __str__(self):
        return self.user_email.email


class order_history(models.Model):
    my_user_id = models.ForeignKey(user,on_delete=models.CASCADE)
    my_order_id = models.ForeignKey(user_order_id,on_delete=models.CASCADE)
    amount = models.CharField(max_length=500)
    transection_id = models.CharField(max_length=500,blank=True,null=True)
    txn_status = models.CharField(max_length=500,default="pending")
    order_history_created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.my_user_id.email


# class user_query(models.Model):
#     name = models.CharField(max_length=250)
#     email = models.CharField(max_length=250)
#     subject = models.CharField(max_length=250)
#     message = models.CharField(max_length=250)