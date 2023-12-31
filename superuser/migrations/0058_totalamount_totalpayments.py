# Generated by Django 3.2.13 on 2022-06-13 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0057_assignpaymentduration_total_invoices'),
    ]

    operations = [
        migrations.CreateModel(
            name='TotalAmount',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TotalPayments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('payment', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
