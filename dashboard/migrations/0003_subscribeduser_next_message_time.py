# Generated by Django 3.2.7 on 2021-10-03 09:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_subscribeduser_prefered_frequency'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribeduser',
            name='next_message_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]