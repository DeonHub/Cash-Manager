# Generated by Django 3.2.13 on 2022-06-25 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0074_makepayment_donation_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='makepayment',
            name='credit',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='makepayment',
            name='donation_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='makepayment',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='makepayment',
            name='install_range',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='makepayment',
            name='subscription_expiry',
            field=models.DateField(blank=True, null=True),
        ),
    ]
