# Generated by Django 3.2.12 on 2022-03-16 05:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CNY',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('price', models.CharField(blank=True, max_length=50, null=True)),
                ('predicted_price', models.CharField(blank=True, max_length=50, null=True)),
                ('dateTimeStamp', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
        ),
        migrations.CreateModel(
            name='Euro',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('price', models.CharField(blank=True, max_length=50, null=True)),
                ('predicted_price', models.CharField(blank=True, max_length=50, null=True)),
                ('dateTimeStamp', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
        ),
        migrations.CreateModel(
            name='GBP',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('price', models.CharField(blank=True, max_length=50, null=True)),
                ('predicted_price', models.CharField(blank=True, max_length=50, null=True)),
                ('dateTimeStamp', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
        ),
        migrations.CreateModel(
            name='Gold',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('price', models.CharField(blank=True, max_length=50, null=True)),
                ('predicted_price', models.CharField(blank=True, max_length=50, null=True)),
                ('dateTimeStamp', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
        ),
        migrations.CreateModel(
            name='JPY',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('price', models.CharField(blank=True, max_length=50, null=True)),
                ('predicted_price', models.CharField(blank=True, max_length=50, null=True)),
                ('dateTimeStamp', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
        ),
    ]
