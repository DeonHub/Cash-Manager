# Generated by Django 3.2.13 on 2022-12-03 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0100_servicefee'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicefee',
            name='paid',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
