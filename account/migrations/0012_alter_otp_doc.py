# Generated by Django 4.2.1 on 2023-05-20 21:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_otp_doc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='doc',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 20, 21, 58, 29, 477507, tzinfo=datetime.timezone.utc)),
        ),
    ]