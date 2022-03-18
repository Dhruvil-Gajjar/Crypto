# Generated by Django 3.2.12 on 2022-03-16 05:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('stripeCustomerId', models.CharField(max_length=255, verbose_name='Stripe Customer Id')),
                ('stripeSubscriptionId', models.CharField(max_length=255, verbose_name='Stripe Subscription Id')),
                ('order_created_at', models.DateTimeField(blank=True, null=True, verbose_name='Order Created at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]