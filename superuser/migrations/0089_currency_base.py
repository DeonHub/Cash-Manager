# Generated by Django 3.2.13 on 2022-09-03 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0088_members_subscriber'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='base',
            field=models.BooleanField(default=False),
        ),
    ]
