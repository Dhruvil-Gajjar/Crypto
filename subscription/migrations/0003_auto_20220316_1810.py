# Generated by Django 3.2.12 on 2022-03-16 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0002_orderhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='productName',
            field=models.CharField(default=1, max_length=256, verbose_name='Product Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='subscriptionEndDate',
            field=models.CharField(default=1, max_length=50, verbose_name='Subscription Start Date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='subscriptionStartDate',
            field=models.CharField(default=1, max_length=50, verbose_name='Subscription Start Date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderhistory',
            name='productName',
            field=models.CharField(default=1, max_length=256, verbose_name='Product Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderhistory',
            name='subscriptionEndDate',
            field=models.CharField(default=1, max_length=50, verbose_name='Subscription Start Date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderhistory',
            name='subscriptionStartDate',
            field=models.CharField(default=1, max_length=50, verbose_name='Subscription Start Date'),
            preserve_default=False,
        ),
    ]
