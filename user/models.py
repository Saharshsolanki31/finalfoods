from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

# Model For User Data
class user(models.Model):
    email = models.CharField(max_length=250)
    phone = models.CharField(max_length=250,null=True)
    password = models.CharField(max_length=250)
    image=models.ImageField(upload_to='media/user_image/',default="user_image/default.png",blank=True,null=True)

class BookTable(models.Model):
    restaurant_name=models.CharField(max_length=500,default="shree nath")
    rest_id=models.CharField(max_length=200,default="1")
    user_name = models.CharField(max_length=500)
    user_contact = models.CharField(max_length=500)
    user_email = models.ForeignKey(user,on_delete=models.CASCADE)
    date = models.DateField(max_length=500)
    time = models.TimeField(max_length=500)
    guests = models.CharField(max_length=500)
    status=models.CharField(max_length=500,default="pending")
    def __str__(self):
        return self.user_name

# class user_query(models.Model):
#     name = models.CharField(max_length=250)
#     email = models.CharField(max_length=250)
#     subject = models.CharField(max_length=250)
#     message = models.CharField(max_length=250)