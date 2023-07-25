from django.contrib import admin
from .models import *


# Register your models here.
@admin.register( 
    AssignPeriod, 
    FeeType, 
    FeeItems, 
    FeeDescription, 
    Currency, 
    InvoiceDetails, 
    Invoice, 
    AssignPaymentDuration, 
    MakePayment, 
    # Message, 
    TotalAmount, 
    TotalPayments, 
    ActivityLog, 
    Balance, 
    # Members, 
    Donation, 
    PublicDonation, 
    PublicPayments,
    PrinterInvoice,
    PrinterDonation,
    Usercode,
    ServiceFee,
    OnlinePayments,
    OfflinePayments
    )

class AppAdmin(admin.ModelAdmin):
    pass