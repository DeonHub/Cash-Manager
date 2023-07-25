# Generated by Django 3.2.13 on 2022-06-22 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0061_rename_messages_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100, null=True)),
                ('action', models.CharField(max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
