# Generated by Django 4.0.4 on 2022-06-03 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0036_alter_makepayment_arrears'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='total_amount',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
