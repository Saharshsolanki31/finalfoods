# Generated by Django 3.2.5 on 2021-07-02 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=250)),
                ('phone', models.CharField(max_length=250, null=True)),
                ('password', models.CharField(max_length=250)),
            ],
        ),
    ]