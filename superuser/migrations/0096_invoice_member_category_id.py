# Generated by Django 3.2.13 on 2022-11-16 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0095_auto_20221116_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='member_category_id',
            field=models.CharField(default='1', max_length=100),
        ),
    ]
