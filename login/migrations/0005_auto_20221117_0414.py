# Generated by Django 3.2.13 on 2022-11-17 04:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20221117_0244'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100, null=True)),
                ('email', models.CharField(default='None', max_length=100, null=True)),
                ('password', models.CharField(default='None', max_length=100, null=True)),
                ('account_name', models.CharField(default='Demo Account', max_length=200, null=True)),
                ('branch', models.CharField(default='Main', max_length=200, null=True)),
                ('expiry_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('pid', models.CharField(default=0, max_length=200, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='clientdetails',
            name='firstname',
            field=models.CharField(default='None', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientdetails',
            name='phone',
            field=models.CharField(default='None', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientdetails',
            name='surname',
            field=models.CharField(default='None', max_length=100, null=True),
        ),
    ]
