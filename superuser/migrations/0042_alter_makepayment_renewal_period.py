# Generated by Django 4.0.4 on 2022-06-03 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0041_alter_makepayment_amount_paid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='makepayment',
            name='renewal_period',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
