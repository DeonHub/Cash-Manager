# Generated by Django 3.2.13 on 2022-06-28 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0081_clients_organizationalmembers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicpayments',
            name='target_amount',
        ),
    ]
