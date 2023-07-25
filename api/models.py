from django.db import models
from django.utils import timezone

# Create your models here.
class Token(models.Model):
    token = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.token

class Dasho(models.Model):
    pid = models.IntegerField(null=True, default=0)
    redirected = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.pid} was redirected = {self.redirected}'



class Dasha(models.Model):
    mid = models.IntegerField(null=True, default=0)
    redirected = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.mid} was redirected = {self.redirected}'



class Name(models.Model):
    name = models.CharField(max_length=500, null=True)
    

    def __str__(self):
        return self.name   


class Nameken(models.Model):
    token = models.CharField(max_length=500, null=True)
    name = models.CharField(max_length=500, null=True)
    role = models.CharField(max_length=100, null=True)
    expiry_date = models.DateField(blank=True, null=True, default=timezone.now)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.name, self.token           