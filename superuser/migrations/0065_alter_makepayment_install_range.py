# Generated by Django 3.2.13 on 2022-06-24 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0064_auto_20220623_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='makepayment',
            name='install_range',
            field=models.CharField(default='Day(s)', max_length=100, null=True),
        ),
    ]