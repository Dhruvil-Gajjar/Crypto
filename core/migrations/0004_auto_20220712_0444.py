# Generated by Django 3.2.12 on 2022-07-12 04:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20220402_1010'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cny',
            options={'verbose_name_plural': 'CNY'},
        ),
        migrations.AlterModelOptions(
            name='euro',
            options={'verbose_name_plural': 'Euro'},
        ),
        migrations.AlterModelOptions(
            name='gbp',
            options={'verbose_name_plural': 'GBP'},
        ),
        migrations.AlterModelOptions(
            name='gold',
            options={'verbose_name_plural': 'Gold'},
        ),
        migrations.AlterModelOptions(
            name='jpy',
            options={'verbose_name_plural': 'JPY'},
        ),
        migrations.AlterModelOptions(
            name='predictiondata',
            options={'verbose_name_plural': 'Prediction Values'},
        ),
    ]
