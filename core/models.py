import uuid
from django.db import models


class Gold(models.Model):
    id = models.CharField(primary_key=True, max_length=36, editable=False, default=uuid.uuid4)
    price = models.CharField(max_length=50, null=True, blank=True)
    predicted_price = models.CharField(max_length=50, null=True, blank=True)
    dateTimeStamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


class Euro(models.Model):
    id = models.CharField(primary_key=True, max_length=36, editable=False, default=uuid.uuid4)
    price = models.CharField(max_length=50, null=True, blank=True)
    predicted_price = models.CharField(max_length=50, null=True, blank=True)
    dateTimeStamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


class JPY(models.Model):
    id = models.CharField(primary_key=True, max_length=36, editable=False, default=uuid.uuid4)
    price = models.CharField(max_length=50, null=True, blank=True)
    predicted_price = models.CharField(max_length=50, null=True, blank=True)
    dateTimeStamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


class CNY(models.Model):
    id = models.CharField(primary_key=True, max_length=36, editable=False, default=uuid.uuid4)
    price = models.CharField(max_length=50, null=True, blank=True)
    predicted_price = models.CharField(max_length=50, null=True, blank=True)
    dateTimeStamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


class GBP(models.Model):
    id = models.CharField(primary_key=True, max_length=36, editable=False, default=uuid.uuid4)
    price = models.CharField(max_length=50, null=True, blank=True)
    predicted_price = models.CharField(max_length=50, null=True, blank=True)
    dateTimeStamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)
