# Generated by Django 3.2.13 on 2022-06-08 04:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0054_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]