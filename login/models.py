from django.db import models
from django.utils import timezone

# Create your models here.
class ClientDetails(models.Model):
    session_id = models.CharField(max_length=100, null=True)
    token = models.CharField(max_length=100, null=True)
    firstname = models.CharField(max_length=100, null=True, default="None")
    surname = models.CharField(max_length=100, null=True, default="None")
    fullname = models.CharField(max_length=100, null=True, default="None")
    phone = models.CharField(max_length=100, null=True, default="None")
    email = models.CharField(max_length=100, null=True, default="None")
    password = models.CharField(max_length=100, null=True, default="None")
    account_name = models.CharField(max_length=200, null=True, default="Demo Account")
    branch = models.CharField(max_length=200, null=True, default="Main")
    expiry_date = models.DateField(blank=True, null=True, default=timezone.now)
    pid = models.CharField(max_length=200, null=True, default=0)
    userId = models.CharField(max_length=200, null=True, default=0)
    unlimited = models.BooleanField(blank=True, null=True, default=False)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.account_name 


class MemberDetails(models.Model):
    token = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True, default="None")
    password = models.CharField(max_length=100, null=True, default="None")
    client_id = models.CharField(max_length=100, null=True, default="1")
    account_name = models.CharField(max_length=200, null=True, default="Demo Account")
    branch = models.CharField(max_length=200, null=True, default="Main")
    expiry_date = models.DateField(blank=True, null=True, default=timezone.now)
    mid = models.CharField(max_length=200, null=True, default=0)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.account_name