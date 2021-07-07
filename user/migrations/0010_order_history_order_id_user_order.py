# Generated by Django 3.2.5 on 2021-07-07 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_restaurant_restaurant_description'),
        ('user', '0009_auto_20210707_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='order_id',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=500)),
                ('order_type', models.CharField(max_length=500)),
                ('status', models.CharField(default='pending', max_length=500)),
                ('pickup_time', models.CharField(blank=True, max_length=500, null=True)),
                ('order_id_created_at', models.DateTimeField(auto_now_add=True)),
                ('address_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.address')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='user_order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_quantity', models.CharField(default='1', max_length=500)),
                ('food_total_price', models.CharField(default='0', max_length=500)),
                ('food_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.food_item')),
                ('user_email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
                ('user_order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.order_id')),
            ],
        ),
        migrations.CreateModel(
            name='order_history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transection_id', models.CharField(blank=True, max_length=500, null=True)),
                ('txn_status', models.CharField(default='pending', max_length=500)),
                ('order_history_created_at', models.DateTimeField(auto_now_add=True)),
                ('address_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.address')),
                ('food_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.food_item')),
                ('my_order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.order_id')),
                ('my_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]
