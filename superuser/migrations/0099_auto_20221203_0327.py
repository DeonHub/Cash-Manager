# Generated by Django 3.2.13 on 2022-12-03 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0098_auto_20221129_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignpaymentduration',
            name='invoice_type',
            field=models.CharField(default='expiry', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='invoice_type',
            field=models.CharField(default='expiry', max_length=100),
        ),
        migrations.AddField(
            model_name='makepayment',
            name='invoice_type',
            field=models.CharField(default='expiry', max_length=100, null=True),
        ),
    ]
