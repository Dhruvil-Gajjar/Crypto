# Generated by Django 3.2.12 on 2022-07-12 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0004_auto_20220402_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='is_canceled',
            field=models.BooleanField(default=False, verbose_name='Is Canceled'),
        ),
    ]
