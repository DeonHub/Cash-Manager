# Generated by Django 3.2.13 on 2022-11-18 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0096_invoice_member_category_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='makepayment',
            name='confirmed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='makepayment',
            name='invoice_id',
            field=models.CharField(blank=True, default='1', max_length=500, null=True),
        ),
    ]
