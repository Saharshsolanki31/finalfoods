# Generated by Django 3.2 on 2021-07-07 05:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=500)),
                ('user_contact', models.CharField(max_length=500)),
                ('date', models.DateField(max_length=500)),
                ('time', models.TimeField(max_length=500)),
                ('guests', models.CharField(max_length=500)),
                ('status', models.CharField(default='pending', max_length=500)),
                ('user_email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]