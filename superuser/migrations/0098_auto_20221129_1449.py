# Generated by Django 3.2.13 on 2022-11-29 14:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0097_auto_20221118_0254'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usercode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=100, null=True)),
                ('member_id', models.CharField(max_length=100, null=True)),
                ('member', models.CharField(max_length=100, null=True)),
                ('usercode', models.CharField(max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='assignpaymentduration',
            name='usercode',
            field=models.CharField(default='PFA00000', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='assignpaymentduration',
            name='end_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='assignpaymentduration',
            name='start_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
