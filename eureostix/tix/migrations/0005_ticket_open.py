# Generated by Django 4.2.11 on 2024-03-19 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tix', '0004_message_added_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='open',
            field=models.BooleanField(default=True),
        ),
    ]
