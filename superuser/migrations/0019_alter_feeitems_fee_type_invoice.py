# Generated by Django 4.0.4 on 2022-05-19 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0018_feeitems_feetype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeitems',
            name='fee_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='superuser.feetype'),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('branch', models.CharField(max_length=100)),
                ('member_category', models.CharField(max_length=100)),
                ('group', models.CharField(max_length=100)),
                ('subgroup', models.CharField(max_length=100)),
                ('items_amount', models.IntegerField()),
                ('fee_description', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='superuser.feedescription')),
                ('fee_items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='superuser.feeitems')),
                ('fee_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='superuser.feetype')),
            ],
        ),
    ]