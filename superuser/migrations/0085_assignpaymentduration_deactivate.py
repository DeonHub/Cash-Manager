# Generated by Django 3.2.13 on 2022-06-28 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0084_rename_date_paid_totalamount_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignpaymentduration',
            name='deactivate',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]