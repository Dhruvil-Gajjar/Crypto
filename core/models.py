import uuid
from django.db import models


class Gold(models.Model):
    id = models.CharField(primary_key=True, max_length=36, editable=False, default=uuid.uuid4)
    price = models.CharField(max_length=50, null=True, blank=True)
    dateTimeStamp = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    is_data_processed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Gold"

    def save(self, *args, **kwargs):
        if getattr(self, 'price', True):
            if "," in str(self.price):
                new_value = float(str(self.price).replace(",", ""))
            else:
                new_value = self.price

            if float(new_value) < 1:
                self.price = "%.2f" % round(1 / float(new_value), 2)
        super(Gold, self).save(*args, **kwargs)


class Euro(models.Model):
    id = models.CharField(primary_key=True, max_length=36, editable=False, default=uuid.uuid4)
    price = models.CharField(max_length=50, null=True, blank=True)
    dateTimeStamp = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    is_data_processed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Euro"


class JPY(models.Model):
    id = models.CharField(primary_key=True, max_length=36, editable=False, default=uuid.uuid4)
    price = models.CharField(max_length=50, null=True, blank=True)
    dateTimeStamp = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    is_data_processed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "JPY"


class CNY(models.Model):
    id = models.CharField(primary_key=True, max_length=36, editable=False, default=uuid.uuid4)
    price = models.CharField(max_length=50, null=True, blank=True)
    dateTimeStamp = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    is_data_processed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "CNY"


class GBP(models.Model):
    id = models.CharField(primary_key=True, max_length=36, editable=False, default=uuid.uuid4)
    price = models.CharField(max_length=50, null=True, blank=True)
    dateTimeStamp = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    is_data_processed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "GBP"


class PredictionData(models.Model):
    id = models.CharField(primary_key=True, max_length=36, editable=False, default=uuid.uuid4)
    price = models.CharField(max_length=50, null=True, blank=True)
    dateTimeStamp = models.DateTimeField(null=True, blank=True)
    commodity = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Prediction Values"
