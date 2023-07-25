# Generated by Django 4.0.4 on 2022-05-19 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0006_alter_feeitems_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeesItems',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fee_items', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('fee_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='superuser.feetype')),
            ],
        ),
    ]