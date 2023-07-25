from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm
from django import forms
from datetime import date
from django.utils import timezone

# from .views import increment_invoice_numberPa


# Create your models here.

class FeeType(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    client = models.CharField(null=True, default="Lord", max_length=100)
    fee_type = models.CharField(max_length= 50)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.fee_type}'


class FeeItems(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    client = models.CharField(null=True, default="Lord", max_length=100)
    fee_type = models.ForeignKey(FeeType, on_delete= models.CASCADE)
    fee_items = models.CharField(max_length = 100)
    date_created = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        return f'{self.fee_items}'


class FeeDescription(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    client = models.CharField(null=True, default="Lord", max_length=100)    
    fee_description = models.CharField(max_length= 100)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.fee_description



class Currency(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    client = models.CharField(null=True, default="Lord", max_length=100)    
    currency = models.CharField(max_length= 100)
    base = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.currency


class Donation(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    client = models.CharField(null=True, default="Lord", max_length=100)    
    donation_name = models.CharField(max_length= 100)
    target_amount = models.IntegerField(null=True, default=0)
    amount_received = models.IntegerField(null=True, default=0)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.donation_name}'


class PrinterDonation(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    client = models.CharField(null=True, default="Lord", max_length=100)    
    donation_name = models.CharField(max_length= 100)
    target_amount = models.IntegerField(null=True, default=0)
    amount_received = models.IntegerField(null=True, default=0)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.donation_name}'


class PublicDonation(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    client = models.CharField(null=True, default="Lord", max_length=100)  
    branch = models.CharField(max_length= 100, null=True, default="Main Branch")
    member_category = models.CharField(max_length= 100, null=True, default="Staff")
    group = models.CharField(max_length= 100, null=True, default="Zone 12")
    subgroup = models.CharField(max_length= 100, null=True, default="Group A")  
    logo = models.ImageField(blank=True, null=True, upload_to='public-uploads/', default='')
    organization_name = models.CharField(max_length= 100)
    donation_name = models.CharField(max_length= 100)
    target_amount = models.IntegerField(null=True, default=0)
    amount_paid = models.IntegerField(default=0, null=True)
    purpose = models.CharField(max_length= 500, null=True)
    contact = models.CharField(max_length= 500, null=True)
    email = models.EmailField(max_length= 500, null=True)
    website = models.URLField(max_length = 200, null=True)
    payment_url = models.URLField(max_length = 200, null=True, default="google.com")
    date_created = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        return f'{self.donation_name}'



class PublicPayments(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    client = models.CharField(null=True, default="Lord", max_length=100)  
    branch = models.CharField(max_length= 100, null=True, default="Main Branch")
    member_category = models.CharField(max_length= 100, null=True, default="Staff")
    group = models.CharField(max_length= 100, null=True, default="Zone 12")
    subgroup = models.CharField(max_length= 100, null=True, default="Group A")  
    donation_name = models.CharField(max_length= 100)
    amount_paid = models.IntegerField(default=0, null=True)
    donors_name = models.CharField(max_length= 500, null=True)
    contact = models.CharField(max_length= 500, null=True)
    email = models.EmailField(max_length= 500, null=True)
    country = models.CharField(max_length= 500, null=True)
    currency = models.CharField(max_length= 500, null=True)
    remarks = models.CharField(max_length= 100, null=True)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.amount_paid} paid for {self.donation_name}'



class Invoice(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    client = models.CharField(null=True, default="Lord", max_length=100)    
    branch = models.CharField(max_length= 100)
    member_category = models.CharField(max_length= 100)
    group = models.CharField(max_length= 100)
    branch_id= models.CharField(max_length= 100, default="1")
    group_id= models.CharField(max_length= 100, default="1")
    subgroup_id= models.CharField(max_length= 100, default="1")
    member_category_id= models.CharField(max_length= 100, default="1")
    subgroup = models.CharField(max_length= 100)
    fee_type = models.ForeignKey(FeeType, on_delete= models.SET_NULL, null=True)
    fee_description = models.ForeignKey(FeeDescription, on_delete= models.SET_NULL, null=True)
    fee_items = models.ManyToManyField(FeeItems)
    items_amount = models.CharField(max_length= 100)
    total_amount = models.IntegerField(default=0, null=True)
    invoice_type = models.CharField(max_length= 100, default="expiry")
    member_type = models.CharField(max_length= 100, default="individual")
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.branch}, {self.member_category}, {self.group}, {self.subgroup}, {self.fee_type}, {self.fee_description},'


class PrinterInvoice(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    client = models.CharField(null=True, default="Lord", max_length=100)    
    branch = models.CharField(max_length= 100)
    member_category = models.CharField(max_length= 100)
    group = models.CharField(max_length= 100)
    subgroup = models.CharField(max_length= 100)
    fee_type = models.ForeignKey(FeeType, on_delete= models.SET_NULL, null=True)
    fee_description = models.ForeignKey(FeeDescription, on_delete= models.SET_NULL, null=True)
    fee_items = models.ManyToManyField(FeeItems)
    items_amount = models.CharField(max_length= 100)
    total_amount = models.IntegerField(default=0, null=True)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.branch}, {self.member_category}, {self.group}, {self.subgroup}, {self.fee_type}, {self.fee_description},'



# logo and signature upload

class InvoiceDetails(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    client = models.CharField(null=True, default="Lord", max_length=100)    
    signers_name = models.CharField(max_length= 500)
    company_name = models.CharField(max_length= 500, default="Akwaaba Solutions Agency", null=True)
    signature = models.ImageField(blank=True, null=True, upload_to='signature-uploads/', default='')
    logo = models.ImageField(blank=True, null=True, upload_to='logo-uploads/', default='')
    email = models.EmailField(max_length= 500)
    contact = models.CharField(max_length= 500)

    postal_address = models.CharField(max_length= 500, null=True, default="P.O Box 1")
    digital_address = models.CharField(max_length= 500, null=True, default="GA-1234-567")
    website = models.CharField(max_length= 500, null=True, default="https://google.com")
    location = models.CharField(max_length= 500, null=True, default="Accra")

    whatsapp = models.CharField(max_length= 500, null=True, default="233000000000")
    telegram = models.CharField(max_length= 500, null=True, default="233000000000")
    facebook = models.CharField(max_length= 500, null=True, default="@akwaaba.com")
    twitter = models.CharField(max_length= 500, null=True, default="@akwaaba.com")
    instagram = models.CharField(max_length= 500, null=True, default="@akwaaba.com")

    about = models.CharField(max_length= 1000, null=True, default="None")
    services = models.CharField(max_length= 1000, null=True, default="None")



    def __str__(self):
        return f'{self.signers_name}, {self.contact}'



class AssignPeriod(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    client = models.CharField(null=True, default="Lord", max_length=100)    
    name = models.CharField(max_length= 100)

    def __str__(self):
        return f'{self.name}'


class Usercode(models.Model):
    client_id = models.CharField(null=True, max_length=100)
    member_id = models.CharField(null=True, max_length=100)
    member = models.CharField(max_length= 100, null=True)
    usercode = models.CharField(null=True, max_length=100)
    date_created = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        return f'{self.member} - {self.usercode}'


class AssignPaymentDuration(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    member_id = models.CharField(null=True, default="1", max_length=100)
    branch = models.CharField(max_length= 100, null=True)
    member_category = models.CharField(max_length= 100, null=True)
    group = models.CharField(max_length= 100, null=True)
    subgroup = models.CharField(max_length= 100, null=True)
    member = models.CharField(max_length= 100, null=True)
    donation_name = models.CharField(max_length= 100, null=True, default="None")
    
    usercode = models.CharField(null=True, default="PFA00000", max_length=100)

    fee_type = models.ForeignKey(FeeType, on_delete= models.SET_NULL, null=True)
    fee_description = models.ForeignKey(FeeDescription, on_delete= models.SET_NULL, null=True)
    total_invoice = models.IntegerField(blank=True, null=True)
    install_range = models.CharField(max_length= 100, default= None , null=True)
    install_period = models.IntegerField(blank=True, null=True)
    install_amount = models.IntegerField(blank=True, null=True)
    expiration_bill = models.IntegerField(blank=True, null=True)
    set_pay_date =  models.DateField(blank=True, null=True, default=timezone.now)
    start_date =  models.DateField(blank=True, null=True, default=timezone.now)
    end_date =  models.DateField(blank=True, null=True, default=timezone.now)
    amount_by_days = models.IntegerField(blank=True, null=True, default=10)
    deactivate = models.BooleanField(blank=True, null=True, default=True)
    account_status = models.CharField(max_length= 100, null=True)
    invoice_type = models.CharField(max_length= 100, null=True, default="expiry")
    auto = models.BooleanField(null=True, default=False)
    date_created = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        return f'{self.member} - {self.total_invoice}, {self.fee_type}'


class MakePayment(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    member_id = models.CharField(null=True, default="1", max_length=100)
    branch = models.CharField(max_length= 100, null=True)
    member_category = models.CharField(max_length= 100, null=True)
    group = models.CharField(max_length= 100, null=True)
    subgroup = models.CharField(max_length= 100, null=True)
    member = models.CharField(max_length= 100, null=True)

    fee_type = models.ForeignKey(FeeType, on_delete= models.SET_NULL, null=True)
    fee_type_value = models.CharField(null=True, default="none", max_length=100)

    fee_description = models.ForeignKey(FeeDescription, on_delete= models.SET_NULL, null=True)
    fee_description_value = models.CharField(null=True, default="none", max_length=100)

    outstanding_bill = models.IntegerField(blank=True, null=True)
    payers_first_name = models.CharField(max_length= 100, null=True)
    payers_last_name = models.CharField(max_length= 100, null=True)
    contact = models.CharField(max_length= 100, null=True)
    email_address = models.EmailField(max_length= 500, null=True)
    remarks = models.CharField(max_length= 100, null=True)
    user_type = models.CharField(max_length= 100, null=True)
    assigned_duration = models.CharField(max_length=100,  null=True)

    donation_name = models.CharField(max_length= 100, null=True)

    install_range = models.CharField(max_length= 100, null=True)
    install_period = models.IntegerField(blank=True, null=True, default= 1)

    renewal_bill = models.IntegerField(blank=True, null=True)
    expiration_bill = models.IntegerField(blank=True, null=True)
    total_amount_due = models.IntegerField(blank=True, null=True)
    outstanding_balance = models.IntegerField(blank=True, null=True, default=10)
    invoice_type = models.CharField(max_length= 100, null=True, default="expiry")
    amount_paid = models.IntegerField(blank=True, null=True)
    amount_left = models.IntegerField(blank=True, null=True, default=0)

    payment_status = models.CharField(max_length=100, null=True)
    arrears = models.IntegerField(blank=True, null=True)
    credit = models.IntegerField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    subscription_expiry = models.DateField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add= True)
    invoice_no = models.CharField(max_length=500, default="FMS2022661", null=True, blank=True)
    invoice_id = models.CharField(max_length=500, default="1", null=True, blank=True)
    confirmed = models.BooleanField(null=True, default=False)


    def __str__(self):
        return f"{self.payers_first_name} {self.payers_last_name} paid for {self.member}-{self.total_amount_due}, {self.payment_status}"


class SubcriptionPayment(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    client = models.CharField(null=True, default="Lord", max_length=100)
    member = models.CharField(max_length= 100, null=True)
    description = models.CharField(max_length= 100, null=True)
    duration = models.CharField(max_length= 100, null=True)
    renewing_days = models.IntegerField( null=True)
    amount_paid = models.IntegerField(blank=True, null=True)
    subscription_expiry =  models.DateField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.description





class Balance(models.Model):
    member_id = models.CharField(null=True, default="1", max_length=100)
    member = models.CharField(max_length= 100, null=True)
    credit = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.member} has a balance of {self.credit}"



# class Members(models.Model):
#     client_id = models.CharField(null=True, default="1", max_length=100)
#     member_id = models.IntegerField(blank=True, null=True)
#     member = models.CharField(max_length= 100, null=True)
#     profile_url = models.CharField(max_length= 100, null=True)
#     contact = models.CharField(max_length= 100, null=True)
#     email_address = models.EmailField(max_length= 500, null=True)
#     level = models.IntegerField(blank=True, null=True)
#     status = models.IntegerField(blank=True, null=True)
#     account_type = models.IntegerField(blank=True, null=True)
#     member_type = models.IntegerField(blank=True, null=True)
#     branch = models.IntegerField(blank=True, null=True)
#     recently_paid = models.DateField(blank=True, null=True, default=timezone.now)
#     subscriber = models.BooleanField(blank=True, null=True, default=False)

#     def __str__(self):
#         return f"{self.member} paid on {self.recently_paid}"


class OrganizationalMembers(models.Model):
    organization_id = models.IntegerField(blank=True, null=True)
    organization = models.CharField(max_length= 100, null=True)
    profile_url = models.CharField(max_length= 100, null=True)
    contact = models.CharField(max_length= 100, null=True)
    email_address = models.EmailField(max_length= 500, null=True)
    level = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    account_type = models.IntegerField(blank=True, null=True)
    member_type = models.IntegerField(blank=True, null=True)
    branch = models.IntegerField(blank=True, null=True)
    recently_paid = models.DateField(blank=True, null=True, default=timezone.now)

    def __str__(self):
        return f"{self.member} paid on {self.recently_paid}"


# class Clients(models.Model):
#     client_id = models.IntegerField(blank=True, null=True)
#     client = models.CharField(max_length= 100, null=True)
#     profile_url = models.CharField(max_length= 100, null=True)
#     contact = models.CharField(max_length= 100, null=True)
#     email_address = models.EmailField(max_length= 500, null=True)
#     level = models.IntegerField(blank=True, null=True)
#     status = models.IntegerField(blank=True, null=True)
#     account_type = models.IntegerField(blank=True, null=True)
#     member_type = models.IntegerField(blank=True, null=True)
#     branch = models.IntegerField(blank=True, null=True)
#     recently_paid = models.DateField(blank=True, null=True, default=timezone.now)

#     def __str__(self):
#         return f"{self.member} paid on {self.recently_paid}"



# class Count(models.Model):
#     count = models.IntegerField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.count}"


# class ClientCount(models.Model):
#     count = models.IntegerField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.count}"


# class Message(models.Model):
#     client_id = models.CharField(null=True, default="1", max_length=100)
#     client = models.CharField(null=True, default="Lord", max_length=100)    
#     sms = models.CharField(max_length= 500)
#     message = models.CharField(max_length= 500)
#     audio_file = models.FileField(blank=True, null=True, upload_to='audio-uploads/', default='')
#     contact = models.CharField(max_length= 100, null=True)
#     date_created = models.DateTimeField(auto_now_add= True)


#     def __str__(self):
#         return f"{self.sms} sent to {self.contact} on {self.date_created}"


class TotalAmount(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    member_id = models.CharField(null=True, default="1", max_length=100)
    member = models.CharField(max_length= 100, null=True, default="")
    total = models.IntegerField(blank=True, null=True)
    branch = models.CharField(max_length= 100, null=True, default="Main Branch")
    member_category = models.CharField(max_length= 100, null=True, default="Staff")
    group = models.CharField(max_length= 100, null=True, default="Zone 12")
    subgroup = models.CharField(max_length= 100, null=True, default="Group A")
    date_created = models.DateField(blank=True, null=True, default=timezone.now)


    def __str__(self):
        return f"{self.member} was assigned GHc {self.total}"
        
class TotalPayments(models.Model):

    client_id = models.CharField(null=True, default="1", max_length=100)
    member_id = models.CharField(null=True, default="1", max_length=100)
    member = models.CharField(max_length= 100, null=True, default="")
    payment = models.IntegerField(blank=True, null=True)
    branch = models.CharField(max_length= 100, null=True, default="Main Branch")
    member_category = models.CharField(max_length= 100, null=True, default="Staff")
    group = models.CharField(max_length= 100, null=True, default="Zone 12")
    subgroup = models.CharField(max_length= 100, null=True, default="Group A")
    date_created = models.DateField(blank=True, null=True, default=timezone.now)


    def __str__(self):
        return f"{self.member_id}, GHc {self.payment} on {self.date_created}"


class ActivityLog(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    client = models.CharField(null=True, default="Lord", max_length=100)    
    branch = models.CharField(null=True, default="Main Branch", max_length=100)    
    user = models.CharField(max_length= 100, null=True)
    action = models.CharField(max_length= 100, null=True)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"{self.user} {self.action}"


class ServiceFee(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    amount = models.FloatField(blank=True, null=True)
    paid = models.BooleanField(blank=True, null=True, default=False)

    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"{self.client_id} - {self.amount}"



class OnlinePayments(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    branch = models.CharField(max_length= 100, null=True)
    member_category = models.CharField(max_length= 100, null=True)
    group = models.CharField(max_length= 100, null=True)
    subgroup = models.CharField(max_length= 100, null=True)
    total = models.FloatField(blank=True, null=True, default=0.00)
    date_created = models.DateField(auto_now_add= True)


    def __str__(self):
        return f"Client {self.client_id} has recieved a total GHc{self.total} online"


class OfflinePayments(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    branch = models.CharField(max_length= 100, null=True)
    member_category = models.CharField(max_length= 100, null=True)
    group = models.CharField(max_length= 100, null=True)
    subgroup = models.CharField(max_length= 100, null=True)
    total = models.FloatField(blank=True, null=True, default=0.00)
    date_created = models.DateField(auto_now_add= True)


    def __str__(self):
        return f"Client {self.client_id} has recieved a total GHc{self.total} offline"     