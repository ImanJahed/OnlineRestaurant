# Generated by Django 4.2.7 on 2024-01-13 07:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcode',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 13, 7, 29, 5, 645308, tzinfo=datetime.timezone.utc)),
        ),
    ]
