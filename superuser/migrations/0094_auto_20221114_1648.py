# Generated by Django 3.2.13 on 2022-11-14 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0093_auto_20221114_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='totalamount',
            name='client_id',
            field=models.CharField(default='1', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='totalpayments',
            name='client_id',
            field=models.CharField(default='1', max_length=100, null=True),
        ),
    ]
