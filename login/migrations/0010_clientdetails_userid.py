# Generated by Django 3.2.13 on 2023-03-01 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_auto_20230301_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientdetails',
            name='userId',
            field=models.CharField(default=0, max_length=200, null=True),
        ),
    ]
