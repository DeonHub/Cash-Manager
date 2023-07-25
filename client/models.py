from django.db import models
from superuser.models import FeeType, FeeDescription
from django.utils import timezone


# Create your models here.
class Payments(models.Model):
    id = models.AutoField(primary_key=True)
    branch = models.CharField(max_length= 100, null=True)
    member_category = models.CharField(max_length= 100, null=True)
    group = models.CharField(max_length= 100, null=True)
    subgroup = models.CharField(max_length= 100, null=True)
    member = models.CharField(max_length= 100, null=True)
    fee_type = models.ForeignKey(FeeType, on_delete= models.SET_NULL, null=True)
    fee_description = models.ForeignKey(FeeDescription, on_delete= models.SET_NULL, null=True)
    outstanding_bill = models.IntegerField(blank=True, null=True)

    contact = models.CharField(max_length= 100, null=True)
    email_address = models.EmailField(max_length= 500, null=True)

    user_type = models.CharField(max_length= 100, null=True)
    renewal_period = models.CharField(max_length=100,  null=True)
    renewal_bill = models.IntegerField(blank=True, null=True)
    expiration_bill = models.IntegerField(blank=True, null=True)
    total_amount_due = models.IntegerField(blank=True, null=True)
    amount_paid = models.IntegerField(blank=True, null=True)
    payment_status = models.CharField(max_length=100, null=True)
    arrears = models.IntegerField(blank=True, null=True)
    end_date =  models.DateField(blank=True, null=True, default=timezone.now)
    date_created = models.DateTimeField(auto_now_add= True)
    invoice_no = models.CharField(max_length=500, default="FMS2022661", null=True, blank=True)


    def __str__(self):
        return f" {self.member}-{self.total_amount_due}, {self.payment_status}"


# class TotalPayments(models.Model):
#     id = models.AutoField(primary_key=True)
#     member = models.CharField(max_length=100, null=True, blank=True)
#     payment = models.IntegerField(blank=True, null=True)

#     def __str__(self):
#         return f"GHc {self.payment}"