# Generated by Django 3.2.5 on 2021-07-07 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_order_history_amount'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='order_id',
            new_name='user_order_id',
        ),
    ]