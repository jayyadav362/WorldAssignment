# Generated by Django 4.2.1 on 2023-05-20 21:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='doc',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 20, 21, 40, 57, 847995)),
        ),
    ]
