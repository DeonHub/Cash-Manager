# Generated by Django 3.2.13 on 2022-12-09 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_clientdetails_fullname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logdetails',
            name='date_created',
        ),
        migrations.AddField(
            model_name='logdetails',
            name='firstname',
            field=models.CharField(default='None', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='logdetails',
            name='fullname',
            field=models.CharField(default='None', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='logdetails',
            name='phone',
            field=models.CharField(default='None', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='logdetails',
            name='surname',
            field=models.CharField(default='None', max_length=100, null=True),
        ),
    ]
