# Generated by Django 3.2.13 on 2022-06-24 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0065_alter_makepayment_install_range'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member', models.CharField(max_length=100, null=True)),
                ('amount_paid', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
