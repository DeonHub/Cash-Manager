# Generated by Django 3.2.13 on 2022-06-24 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0069_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='count',
            name='count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]