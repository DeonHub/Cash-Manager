# Generated by Django 4.0.4 on 2022-06-02 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0033_rename_setinvoicedetails_invoicedetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='fee_items',
        ),
        migrations.AddField(
            model_name='invoice',
            name='fee_items',
            field=models.ManyToManyField(to='superuser.feeitems'),
        ),
    ]
