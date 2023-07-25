# Generated by Django 3.2.13 on 2023-02-21 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0107_auto_20230221_1856'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ClientCount',
        ),
        migrations.DeleteModel(
            name='Count',
        ),
        migrations.AddField(
            model_name='totalamount',
            name='branch',
            field=models.CharField(default='Main Branch', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='totalamount',
            name='group',
            field=models.CharField(default='Zone 12', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='totalamount',
            name='member_category',
            field=models.CharField(default='Staff', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='totalamount',
            name='subgroup',
            field=models.CharField(default='Group A', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='totalpayments',
            name='branch',
            field=models.CharField(default='Main Branch', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='totalpayments',
            name='group',
            field=models.CharField(default='Zone 12', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='totalpayments',
            name='member_category',
            field=models.CharField(default='Staff', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='totalpayments',
            name='subgroup',
            field=models.CharField(default='Group A', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='assignpaymentduration',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='makepayment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='message',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
