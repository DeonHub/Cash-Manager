# Generated by Django 3.2.13 on 2022-06-24 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0068_members'),
    ]

    operations = [
        migrations.CreateModel(
            name='Count',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
