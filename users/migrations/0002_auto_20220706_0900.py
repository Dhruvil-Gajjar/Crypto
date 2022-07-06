# Generated by Django 3.2.12 on 2022-07-06 09:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='company_name',
            field=models.CharField(blank=True, max_length=256, null=True, validators=[django.core.validators.RegexValidator('[+-/%]', inverse_match=True)]),
        ),
        migrations.AddField(
            model_name='user',
            name='company_size',
            field=models.IntegerField(choices=[(1, '0 - 9'), (2, '10 - 49'), (3, '50 - 249'), (4, '250 - 499'), (5, '500 - 999'), (6, '1000+')], default=1),
        ),
        migrations.AddField(
            model_name='user',
            name='sector',
            field=models.IntegerField(choices=[(1, 'Drop 1'), (2, 'Drop 2')], default=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]