# Generated by Django 3.2.12 on 2022-07-18 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_is_free_trial_used'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='free_trial_start_date',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_free_trial_used',
        ),
        migrations.AlterField(
            model_name='user',
            name='free_trial',
            field=models.BooleanField(default=True),
        ),
    ]