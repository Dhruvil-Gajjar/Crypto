import uuid
from django.db import models
from users.models import User


class Product(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=36,
        editable=False,
        default=uuid.uuid4
    )
    name = models.CharField(
        max_length=70,
        verbose_name='Product Name'
    )
    price = models.IntegerField(
        default=0,
        verbose_name='Product Price'
    )
    billingPeriod = models.CharField(
        max_length=70,
        verbose_name='Billing Period'
    )
    stripeProductId = models.CharField(
        max_length=256,
        verbose_name='Stripe Product Id'
    )

    def __str__(self):
        if self.name:
            return self.name
        return str(self.id)


class OrderDetail(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=36,
        editable=False,
        default=uuid.uuid4
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='User'
    )
    stripeCustomerId = models.CharField(
        max_length=255,
        verbose_name='Stripe Customer Id'
    )
    stripeSubscriptionId = models.CharField(
        max_length=255,
        verbose_name='Stripe Subscription Id'
    )
    productName = models.CharField(
        max_length=256,
        verbose_name='Product Name'
    )
    subscriptionStartDate = models.CharField(
        max_length=50,
        verbose_name='Subscription Start Date'
    )
    subscriptionEndDate = models.CharField(
        max_length=50,
        verbose_name='Subscription End Date'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is Active'
    )
    is_canceled = models.BooleanField(
        default=False,
        verbose_name='Is Canceled'
    )

    def __str__(self):
        if self.user and self.user.first_name and self.user.last_name:
            return self.user.first_name + " " + self.user.last_name
        return str(self.id)

    def plan_price(self):
        if self.productName:
            product_obj = Product.objects.filter(name=str(self.productName).strip()).first()
            if product_obj:
                return product_obj.price
        return ""

    def plan_period(self):
        if self.productName:
            product_obj = Product.objects.filter(name=str(self.productName).strip()).first()
            if product_obj:
                return product_obj.billingPeriod
        return ""


class OrderHistory(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=36,
        editable=False,
        default=uuid.uuid4
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='User'
    )
    stripeCustomerId = models.CharField(
        max_length=255,
        verbose_name='Stripe Customer Id'
    )
    stripeSubscriptionId = models.CharField(
        max_length=255,
        verbose_name='Stripe Subscription Id'
    )
    productName = models.CharField(
        max_length=256,
        verbose_name='Product Name'
    )
    subscriptionStartDate = models.CharField(
        max_length=50,
        verbose_name='Subscription Start Date'
    )
    subscriptionEndDate = models.CharField(
        max_length=50,
        verbose_name='Subscription End Date'
    )
    order_created_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Order Created at'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )

    def __str__(self):
        if self.user and self.user.first_name and self.user.last_name:
            return self.user.first_name + " " + self.user.last_name
        return str(self.id)

    def plan_price(self):
        if self.productName:
            product_obj = Product.objects.filter(name=str(self.productName).strip()).first()
            if product_obj:
                return product_obj.price
        return ""

    def plan_period(self):
        if self.productName:
            product_obj = Product.objects.filter(name=str(self.productName).strip()).first()
            if product_obj:
                return product_obj.billingPeriod
        return ""
