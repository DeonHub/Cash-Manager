# Generated by Django 3.2.13 on 2022-11-16 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0094_auto_20221114_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='branch_id',
            field=models.CharField(default='1', max_length=100),
        ),
        migrations.AddField(
            model_name='invoice',
            name='group_id',
            field=models.CharField(default='1', max_length=100),
        ),
        migrations.AddField(
            model_name='invoice',
            name='subgroup_id',
            field=models.CharField(default='1', max_length=100),
        ),
    ]
