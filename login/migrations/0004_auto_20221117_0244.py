# Generated by Django 3.2.13 on 2022-11-17 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20221117_0117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientdetails',
            name='pid',
            field=models.CharField(default=0, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='memberdetails',
            name='mid',
            field=models.CharField(default=0, max_length=200, null=True),
        ),
    ]