# Generated by Django 3.2.13 on 2023-02-22 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0112_auto_20230222_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='makepayment',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
