# Generated by Django 3.2.13 on 2022-06-25 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0072_makepayment_outstanding_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donation_name', models.CharField(max_length=100)),
                ('target_amount', models.IntegerField(default='Any amount')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='assignpaymentduration',
            name='donation_name',
            field=models.CharField(default='None', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='assignpaymentduration',
            name='account_status',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='assignpaymentduration',
            name='install_range',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
