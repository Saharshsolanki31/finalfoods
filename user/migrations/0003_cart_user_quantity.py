# Generated by Django 3.2.5 on 2021-07-06 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='user_quantity',
            field=models.CharField(default='1', max_length=500),
        ),
    ]
