from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render, get_object_or_404
from login.models import MemberDetails, ClientDetails
from api.models import Dasho
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from dateutil.relativedelta import relativedelta
from django.template.loader import get_template
from reportlab.lib.pagesizes import letter
from django.http import FileResponse
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from django.core import serializers
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from xhtml2pdf import pisa
from .models import *
from .filter import *
import requests
import datetime
import pyshorteners
import json
import io
import os
import csv
import random
import string
import os
import environ
from django.db.models.functions import Length

env = environ.Env()
environ.Env.read_env()




def random_char(y):
    return ''.join(random.choice(string.ascii_uppercase) for x in range(y))


def donors_csv(request, *args, **kwargs):

    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['Donors Name', 'Contact', 'Email Address', 'Country', 'Donation Name', 'Currency', 'Amount Paid', 'Paid On'])


    for donor in PublicPayments.objects.all().values_list('donors_name', 'contact', 'email', 'country', 'donation_name', 'currency', 'amount_paid', 'date_created'):
        writer.writerow(donor)

    response['Content-Disposition'] =  'filename="donors.csv"'

    return response



# def subscribers_csv(request, *args, **kwargs):
    
#     response = HttpResponse(content_type='text/csv')

#     writer = csv.writer(response)
#     writer.writerow(['Member', 'Status', 'Last Paid'])

#     for donor in Members.objects.all().values_list('member', 'subscriber', 'recently_paid'):
#         writer.writerow(donor)

#     response['Content-Disposition'] =  'filename="subscribers.csv"'

#     return response



def invoice_details_view(request, *args, **kwargs):
    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
 
    pk = kwargs.get('pk')

    try:
        base = Currency.objects.get(client_id=client_id, base=True).currency
    except:
        base = "GHS"    
    

    company = InvoiceDetails.objects.filter(client_id=client_id).first()
    detail = get_object_or_404(MakePayment, pk=pk)

    try:
        invoice = Invoice.objects.get(fee_type= detail.fee_type, branch= detail.branch, member_category= detail.member_category, group= detail.group, subgroup= detail.subgroup)
    except:
        try:
            invoice = PrinterInvoice.objects.get(fee_type= detail.fee_type, branch= detail.branch, member_category= detail.member_category, group= detail.group, subgroup= detail.subgroup, total_amount=detail.outstanding_bill)
        except:
            return HttpResponse("Invoice does not exist")    

    keys = [item.fee_items for item in invoice.fee_items.all()]
    values = ["{:,}".format(int(i)) for i in invoice.items_amount.split(',')]
    data = dict(zip(keys, values))

    template_path = 'superuser/user_printer.html'
    context = {
        'detail': detail,
        'company': company, 
        'invoice': invoice,
        'data': data,
        'base':base
         }


    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')


    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
    
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response )

    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def send_mails(request, **kwargs):
    member = request.POST.get('member')

    template = get_template('user_printer.txt')
    context = {
        'member': member,
    }

    message = template.render(context)
    email = EmailMultiAlternatives(
        "Subject", 
        "Message", 
        "impraimgideon89@gmail.com", 
        ["impraimgideon89@gmail.com"] 
        )


    email.content_subtype = "html"
    email.send()

    messages.success(request, "Message sent successfully!")

    return HttpResponseRedirect(reverse('superuser:viewPayments')) 






def donation_details_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
 

    company = InvoiceDetails.objects.filter(client_id=client_id).first()
    detail = get_object_or_404(MakePayment, pk=pk)
    # print(detail)

    try:
        donation = PrinterDonation.objects.get(donation_name=detail.donation_name)
    except:
        donation = PrinterDonation.objects.filter(donation_name=detail.donation_name).first()



    
    # keys = [item.fee_items for item in invoice.fee_items.all()]
    # values = ["{:,}".format(int(i)) for i in invoice.items_amount.split(',')]
    # data = dict(zip(keys, values))

    template_path = 'superuser/donation_printer.html'
    context = {
        'detail': detail,
        'company': company, 
        # 'invoice': invoice,
        # 'data': data
         }


    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')


    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
    
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response )

    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response





def index(request):

    template_name = 'superuser/index.html'
    today = datetime.date.today()
    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch
    unlimited = details.unlimited


    payload = json.dumps({ "phone_email": email, "password": password, "checkDeviceInfo": False })

    headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=Ly8oYWb8c70C2CDUYfFd0poVjCL91Octs99w3q6rGjSu8L2SaPVDoGPvJ4tKQIda; sessionid=4zyr1pvz9r6hyu8sqvuh0gqqxsymo56n'
    }


   
    branch_url = "https://db-api-v2.akwaabasoftware.com/clients/branch"
    branchex = requests.request("GET", branch_url, headers=headers, data=payload).json()['data']



    member_category_url = "https://db-api-v2.akwaabasoftware.com/members/groupings/member-category"
    categories = requests.request("GET", member_category_url, headers=headers, data=payload).json()['data']


    group_url = "https://db-api-v2.akwaabasoftware.com/members/groupings/group"
    groups = requests.request("GET", group_url, headers=headers, data=payload).json()['data']


    subgroup_url = "https://db-api-v2.akwaabasoftware.com/members/groupings/sub-group"
    subgroups = requests.request("GET", subgroup_url, headers=headers, data=payload).json()['data']




    payload = json.dumps({})
    headers = {}

    service_url = f"https://super.akwaabasoftware.com/api/service-fee/{client_id}/"

    try:
        service_charge = requests.request("GET", service_url, headers=headers, data=payload).json()['service_fee']

        outstanding = requests.request("GET", service_url, headers=headers, data=payload).json()['outstanding_fee']
        outstanding = float(outstanding)
    except:
        service_charge = 0
        outstanding = 0.00

   

    try:
        base = Currency.objects.get(client_id=client_id, base=True).currency
        
    except:
        base = 'GHS'


    # try:
    #     details = ClientDetails.objects.get(pid=client_id)
    #     account_name = details.account_name
    #     branch = details.branch
    #     pid = details.pid
    #     token = details.token
    

    #     try:
    #         dasho = Dasho.objects.get(pid=client_id)

    #         if dasho.redirected == True:
    #             setItem = True
    #         else:
    #             setItem = False
    #     except:
    #         setItem = False  


    # except:
    #         token = ""
    #         account_name = "Demoss Account"
    #         branch = "Other Branch"
    #         pid = 1
    #         setItem = False
    #         base = 'GHS'



    # year = 2021

    # request.session['counter'] = counter

    total_invoice=0
    total_payments=0
    public_donations=0
    january_amount=0
    february_amount=0
    march_amount=0
    april_amount=0
    may_amount=0
    june_amount=0
    july_amount=0
    august_amount=0
    september_amount=0
    october_amount=0
    november_amount=0
    december_amount=0

    full_payment = []
    part_payment = []
    active = []
    expired = []


    year_range = request.GET.get('year_range', today.year)
    if year_range:
        year = int(year_range)
    else:
        year = today.year


    branches = request.GET.get('branches', None)
    member_category = request.GET.get('member_category', None)
    group = request.GET.get('group', None)
    subgroup = request.GET.get('subgroup', None)

    # start_date = request.GET.get('start_date', '1990-01-01')
    # end_date = request.GET.get('end_date', str(today))


    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    # print(start_date)

    if start_date or end_date:
        date_format = '%Y-%m-%d'
        start_date = datetime.datetime.strptime(start_date, date_format)
        lastDayStr = datetime.datetime(year, 12, 31).strftime('%Y-%m-%d')

        if year == today.year:
            end_date = datetime.datetime.strptime(end_date, date_format)
        else:   
            end_date = datetime.datetime.strptime(lastDayStr, '%Y-%m-%d') 

        
        
    else:
        firstDayStr = datetime.datetime(year, 1, 1).strftime('%Y-%m-%d')
        lastDayStr = datetime.datetime(year, 12, 31).strftime('%Y-%m-%d')
        
        start_date = datetime.datetime.strptime(firstDayStr, '%Y-%m-%d')


        if year == today.year:
            end_date = today
        else:
            end_date = datetime.datetime.strptime(lastDayStr, '%Y-%m-%d')
        
    # print(end_date)
    # print(year)
    #     # all_payments = MakePayment.objects.filter(date_created__range=[start_date, end_date], confirmed=True).order_by('-id')

    string_start = start_date.strftime("%Y-%m-%d")
    string_end = end_date.strftime("%Y-%m-%d")
    string_today = today.strftime("%Y-%m-%d")




    # Amount Paid by months, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}'

    january = [int(x.amount_paid) for x in MakePayment.objects.filter(client_id=client_id, date_created__month=1, date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}')]
    february = [int(x.amount_paid) for x in MakePayment.objects.filter(client_id=client_id, date_created__month=2, date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}')]
    march = [int(x.amount_paid) for x in MakePayment.objects.filter(client_id=client_id, date_created__month=3, date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}')]
    april = [int(x.amount_paid) for x in MakePayment.objects.filter(client_id=client_id, date_created__month=4, date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}')]
    may = [int(x.amount_paid) for x in MakePayment.objects.filter(client_id=client_id, date_created__month=5, date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}')]
    june = [int(x.amount_paid) for x in MakePayment.objects.filter(client_id=client_id, date_created__month=6, date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}')]
    july = [int(x.amount_paid) for x in MakePayment.objects.filter(client_id=client_id, date_created__month=7, date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}')]
    august = [int(x.amount_paid) for x in MakePayment.objects.filter(client_id=client_id, date_created__month=8, date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}')]
    september = [int(x.amount_paid) for x in MakePayment.objects.filter(client_id=client_id, date_created__month=9, date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}')]
    october = [int(x.amount_paid) for x in MakePayment.objects.filter(client_id=client_id, date_created__month=10, date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}')]
    november = [int(x.amount_paid) for x in MakePayment.objects.filter(client_id=client_id, date_created__month=11, date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}')]
    december = [int(x.amount_paid) for x in MakePayment.objects.filter(client_id=client_id, date_created__month=12, date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}')]
    
    


    for i in january:
        january_amount += i

    for i in february:
        february_amount += i  

    for i in march:
        march_amount += i 

    for i in april:
        april_amount += i  

    for i in may:
        may_amount += i  

    for i in june:
        june_amount += i  

    for i in july:
        july_amount += i

    for i in august:
        august_amount += i

    for i in september:
        september_amount += i

    for i in october:
        october_amount += i

    for i in november:
        november_amount += i

    for i in december:
        december_amount += i  


    temp_invoice = [int(invoice.total) for invoice in TotalAmount.objects.filter(client_id=client_id,  date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}')]
    temp_payments = [int(invoice.payment) for invoice in TotalPayments.objects.filter(client_id=client_id,  date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}')]
        
    payments = []
    nones=[]
    payment = [payment.expiration_bill for payment in AssignPaymentDuration.objects.filter(client_id=client_id, date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}')]
    temp_donations = [int(public_donation.amount_paid) for public_donation in PublicPayments.objects.filter(client_id=client_id, date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}')]

    # no payment
    for x in AssignPaymentDuration.objects.filter(client_id=client_id, date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}'):
        if x.expiration_bill == x.total_invoice:
            nones.append(1)


    for i in payment:
        if i == None:
            pass
        else:
            payments.append(i) 
    # print(payments)           


    end_dates = [payment.end_date for payment in MakePayment.objects.filter(client_id=client_id, date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}')]

    for date in end_dates:
        if date == None:
            pass  
        else:
            if date > today:
                active.append(date)
            else:
                expired.append(date)


    active_users = len(active)
    expired_users = len(expired)

    for i in payments:
        if i > 0:
            part_payment.append(i)
        else:
            full_payment.append(i)    
        
    part_payments = len(part_payment)
    full_payments = len(full_payment)

    for i in temp_donations:
        public_donations += i

    for i in temp_invoice:
        total_invoice += i


    for i in temp_payments:
        total_payments += i

    try:
        collected= (total_payments / total_invoice)*100
    except ZeroDivisionError:
        collected=0

    amount_received= '{0:.2f}'.format(collected)


    
    online = sum([float(invoice.total) for invoice in OnlinePayments.objects.filter(client_id=client_id, date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}' )])
    offline = sum([float(invoice.total) for invoice in OfflinePayments.objects.filter(client_id=client_id, date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}' )])



    expiry_invoices = sum([int(payment.total_invoice) for payment in AssignPaymentDuration.objects.filter(client_id=client_id, invoice_type='expiry', date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}')])
    non_expiry_invoices = sum([int(payment.total_invoice) for payment in AssignPaymentDuration.objects.filter(client_id=client_id, invoice_type='non_expiry', date_created__year=year, date_created__range=[start_date, end_date], branch__regex=r'.+?' if branches == None else fr'{branches}', member_category__regex=r'.+?' if member_category == None else fr'{member_category}', group__regex=r'.+?' if group == None else fr'{group}', subgroup__regex=r'.+?' if subgroup == None else fr'{subgroup}')])



    # Projected Income
    # Projected Expenses
    projected_expenses = 2000


    # Online Collections
    # Cash Collections
    # Total Collections
    # Percentage recieved
    # Total Arrears

    # Total Expenses
    total_expenses = 2000

    # Full Payment Users
    # Part Payment Users
    # Active Users
    # Inactive Users
    # Service Charge
    # Collections After Service Charges
    collections_after_service_charge = 2000
    # Expiry Invoices
    # Non-Expiry Invoices

    total_arrears = total_invoice - total_payments
    string_payments = "{:,}".format(total_payments)
    string_invoice = "{:,}".format(total_invoice)
    string_arrears = "{:,}".format(total_arrears)
    string_donations = "{:,}".format(public_donations)
    string_online = "{:,}".format(online)
    string_offline = "{:,}".format(offline)
    string_expiry_invoices = "{:,}".format(expiry_invoices)
    string_non_expiry_invoices = "{:,}".format(non_expiry_invoices)
    
    # returns = "10%"


    # labels = ["Total Invoice", "Total Collections", "Total Arrears", "Part Payments", "Full Payments", "Active Users", "Expired Users"]
    data1 = [total_invoice, projected_expenses, online, offline, total_payments, amount_received, total_arrears, total_expenses, part_payments, full_payments, active_users, expired_users, outstanding, collections_after_service_charge, expiry_invoices, non_expiry_invoices]
    data2 = [january_amount, february_amount, march_amount, april_amount, may_amount, june_amount, july_amount, august_amount, september_amount, october_amount, november_amount, december_amount]
 
      

    return render(request, template_name, {
                'string_payments':string_payments,
                'string_arrears':string_arrears,
                'string_invoice':string_invoice,
                'string_online':string_online,
                'string_offline':string_offline,
                'string_expiry_invoices':string_expiry_invoices,
                'string_non_expiry_invoices':string_non_expiry_invoices,
                'string_donations': string_donations,
                'public_donations': public_donations,
                'total_invoice': total_invoice,
                'total_payments': total_payments,
                'total_arrears': total_arrears,
                'part_payments': part_payments,
                'full_payments': full_payments,
                'active_users': active_users,
                'expired_users': expired_users,
                'amount_received': amount_received,
                'string_start':string_start,
                'string_end':string_end,
                'string_today':string_today,
                'data1': data1,
                'data2': data2,
                'outstanding':outstanding,
                'client_id': client_id,
                'year': year,
                'year_range': year_range,
                'branches': branches,
                'account_name': account_name, 
                'member_category':member_category,
                'subgroup':subgroup,
                'group':group,
                'branch':branch, 
                'pid':client_id, 
                'token':token, 
                # 'setItem': setItem, 
                'base': base,
                'start_date':start_date,
                'end_date':end_date,
                'service_charge': service_charge,
                'branchex':branchex,
                'categories':categories,
                'groups':groups,
                'subgroups':subgroups,
                'session_id':session_id,
                'unlimited': unlimited,
            })  







# Create your views here.
# Fee Type Views
# Create Fee types
def createFeeType(request, **kwargs):
    template_name = 'superuser/create-fee-type.html'
    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
 
    fullname = details.fullname  
    account_name = details.account_name
    branch = details.branch


    if request.method == 'POST':

        fee_types = request.POST.get('fee_type')
       

        if ',' in fee_types:
            fee_types = fee_types.split(',')

            for fee in fee_types:
                fee_type = FeeType(fee_type=fee, client_id=client_id, client=fullname)
                fee_type.save()

            activity = ActivityLog(user=fullname, client_id=client_id, branch=branch, action=f'created fee type(s) {",".join(fee_types)}')    
            activity.save()
        else:
            fee_type = FeeType(fee_type=fee_types, client_id=client_id, client=fullname)
            fee_type.save()

            activity = ActivityLog(user=fullname, client_id=client_id, branch=branch, action=f'created fee type {fee_types}')    
            activity.save()

        messages.success(request, 'Fee Type(s) created successfully!')
        # return redirect(reverse('superuser:viewFeeType')) 

        return redirect('superuser:viewFeeType') 
    else:
        return render(request, template_name, {
            'pid': client_id,
            'branch':branch,
            'account_name':account_name,
            'session_id':session_id,
            
        })




# View fee type

def viewFeeType(request, **kwargs):
    template_name = 'superuser/view-fee-type.html'
    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid 
    account_name = details.account_name
    branch = details.branch
    unlimited = details.unlimited


    fee_types = FeeType.objects.filter(client_id=client_id)

    return render(request, template_name, {
        'fee_types': fee_types,
        'pid': client_id,
        'branch':branch,
        'account_name':account_name,
        'session_id':session_id,
        'unlimited': unlimited,
    })



# Edit fee type
def editFeeType(request, id, **kwargs):

    fee_type = FeeType.objects.get(id=id)
    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid 
    account_name = details.account_name
    branch = details.branch
    fullname = details.fullname  


    fee_types = FeeType.objects.filter(client_id=client_id).order_by('fee_type')

    
    if request.method == 'POST':
        fee_type.fee_type = request.POST.get('fee_type')
        fee_type.save()

        activity = ActivityLog(user=fullname, client_id=client_id, branch=branch, action=f'edited fee type {fee_type}')    
        activity.save()

        messages.success(request, 'Fee Type edited successfully!')

        return redirect('superuser:viewFeeType') 

    else:
        return render(request, 'superuser/edit-fee-type.html', {
            'fee_type': fee_type,
            'fee_types': fee_types,
            'pid': client_id,
            'branch':branch,
            'account_name':account_name,
            'session_id':session_id,            
        }) 




# Delete fee type
def deleteFeeType(request, id, *args, **kwargs):

    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    branch = details.branch
    fullname = details.fullname  

    if request.method == "POST":
        fee_type = FeeType.objects.get(id=id)
        fee_type.delete()

        activity = ActivityLog(user=fullname, branch=branch, client_id=client_id, action=f'deleted fee type {fee_type}')    
        activity.save()

    messages.success(request, 'Fee Type deleted successfully!')
    return redirect('superuser:viewFeeType')


    




# Create Fee item
def createFeeItems(request, **kwargs):
    template_name = 'superuser/create-fee-items.html'
    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    account_name = details.account_name
    branch = details.branch
    fullname = details.fullname  


    fee_types = FeeType.objects.filter(client_id=client_id)



    if request.method == 'POST':

        fee_type = request.POST.get('fee_type')
        r = FeeType.objects.get(id=fee_type)


        fee_items = request.POST.get('fee_items')

        if ',' in fee_items:
            fee_items = fee_items.split(',')

            for item in fee_items:
                fee_item = FeeItems(fee_type=r, fee_items=item, client_id=client_id, client=fullname)
                fee_item.save()

            activity = ActivityLog(user=fullname, branch=branch, client_id=client_id, action=f'created fee items(s) {",".join(fee_items)}')    
            activity.save()    

        else:
            fee_item = FeeItems(fee_type=r, fee_items=fee_items, client_id=client_id, client=fullname)
            fee_item.save()

            activity = ActivityLog(user=fullname, branch=branch, client_id=client_id, action=f'created fee items {fee_items}')    
            activity.save()
            
            
        messages.success(request, 'Fee Item(s) created successfully!')
        # return HttpResponseRedirect(reverse('superuser:viewFeeItems')) 
        return redirect('superuser:viewFeeItems')

    else:
        return render(request, template_name, {
            'fee_type': fee_types,
            'pid': client_id,
            'branch':branch,
            'account_name':account_name, 
            'session_id':session_id,           
        })        

   


# View fee item

def viewFeeItems(request, **kwargs):

    template_name = 'superuser/view-fee-items.html'
    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid

    account_name = details.account_name
    branch = details.branch
    fullname = details.fullname  
    unlimited = details.unlimited
 

    fee_type = FeeType.objects.filter(client_id=client_id)
    fee_items = FeeItems.objects.filter(client_id=client_id)

    for i in fee_type:
        fee_itemss = FeeItems.objects.filter(fee_type=i, client_id=client_id)

    return render(request, template_name, {
        'fee_items': fee_items,
        'pid': client_id,
        'branch':branch,
        'account_name':account_name,    
        'session_id':session_id,
        'unlimited': unlimited,
    })



# Edit Fee Item
def editFeeItem(request, id, **kwargs):

    
    template_name = 'superuser/edit-fee-item.html'
    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
  
    account_name = details.account_name
    branch = details.branch
    fullname = details.fullname  


    fee_item = FeeItems.objects.get(id=id)
    fee_types = FeeType.objects.filter(client_id=client_id).order_by('-fee_type')
    
    if request.method == 'POST':
        fee_type = request.POST.get('fee_type')
        fee_item.fee_type = FeeType.objects.get(id=fee_type)

        fee_item.fee_items = request.POST.get('fee_items')

        fee_item.save()

        activity = ActivityLog(user=fullname, branch=branch, client_id=client_id, action=f'edited fee item {fee_item}')    
        activity.save()

        messages.success(request, 'Fee Item edited successfully!')

        return redirect('superuser:viewFeeItems')

    

    return render(request, template_name, {
        'fee_item': fee_item,
        'fee_types': fee_types,
        'pid': client_id,
        'branch':branch,
        'account_name':account_name,
        'session_id':session_id,        
    }) 



# Delete Fee Item
def deleteFeeItem(request, id, *args, **kwargs):

    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    branch = details.branch
    fullname = details.fullname  


    if request.method == "POST":
        fee_item = FeeItems.objects.get(id=id)
        fee_item.delete()

        activity = ActivityLog(user=fullname, branch=branch, client_id=client_id, action=f'deleted fee item {fee_item}')    
        activity.save()

    messages.success(request, 'Fee Item deleted successfully!')
    return redirect('superuser:viewFeeItems')
  





# Fee Description Views
# Create fee description
def createFeeDescription(request, **kwargs):

    template_name = 'superuser/create-fee-description.html'
    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    account_name = details.account_name
    branch = details.branch
    fullname = details.fullname  

    if request.method == 'POST':
        fee_descriptions = request.POST.get('fee_description')

        if ',' in fee_descriptions:
            fee_descriptions = fee_descriptions.split(',')

            for description in fee_descriptions:
                fee_description = FeeDescription(fee_description=description, client_id=client_id, client=fullname)
                fee_description.save()

            activity = ActivityLog(user=fullname,branch=branch, client_id=client_id, action=f'created fee description(s) {",".join(fee_descriptions)}')    
            activity.save()    
            # messages.success(request, 'Fee Type created successfully!')
        else:
            fee_description = FeeDescription(fee_description=fee_descriptions, client_id=client_id, client=fullname)
            fee_description.save()

            activity = ActivityLog(user=fullname, branch=branch, client_id=client_id, action=f'created fee description {fee_descriptions}')    
            activity.save()
            
        messages.success(request, 'Fee Description(s) created successfully!')
        return redirect('superuser:viewFeeDescription')

    else:

        return render(request, template_name, {
            'pid': client_id,
            'branch':branch,
            'account_name':account_name,
            'session_id':session_id,            
        })    




# View fee description

def viewFeeDescription(request, **kwargs):
    # if ClientDetails.objects.count() > 0:

    template_name = 'superuser/view-fee-description.html'

    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    account_name = details.account_name
    branch = details.branch
    unlimited = details.unlimited


    fee_descriptions = FeeDescription.objects.filter(client_id=client_id)

    return render(request, template_name, {
        'fee_descriptions': fee_descriptions,
        'pid': client_id,
        'branch':branch,
        'account_name':account_name,
        'session_id':session_id,  
        'unlimited': unlimited,  
    })





# Edit fee description
def editFeeDescription(request, id, **kwargs):

        template_name = 'superuser/edit-fee-description.html'
        fee_description = FeeDescription.objects.get(id=id)
        session_id = request.COOKIES.get('session_id')
        details = ClientDetails.objects.get(session_id=session_id)

        client_id = details.pid

        account_name = details.account_name
        branch = details.branch
        fullname = details.fullname  
        
        if request.method == 'POST':
            fee_description.fee_description = request.POST.get('fee_description')
            fee_description.save()

            activity = ActivityLog(user=fullname, branch=branch, client_id=client_id, action=f'edited fee description {fee_description}')    
            activity.save()

            messages.success(request, 'Fee Description edited successfully!')

            # return HttpResponseRedirect(reverse('superuser:viewFeeDescription')) 
            return redirect('superuser:viewFeeDescription')

        return render(request, template_name, {
            'fee_description': fee_description,
            'pid': client_id,
            'branch':branch,
            'account_name':account_name,
            'session_id':session_id,             
        }) 
  




# Delete fee description
def deleteFeeDescription(request, id, *args, **kwargs):

    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    branch = details.branch
    fullname = details.fullname   

    if request.method == "POST":
        fee_description = FeeDescription.objects.get(id=id)
        fee_description.delete()

        activity = ActivityLog(user=fullname, branch=branch, client_id=client_id, action=f'deleted fee description {fee_description}')    
        activity.save()
        messages.success(request, 'Fee Description deleted successfully!')
        return redirect('superuser:viewFeeDescription')





# Currency Views
# Create Currency
def createCurrency(request, **kwargs):

        template_name = 'superuser/create-currency.html'
        session_id = request.COOKIES.get('session_id')
        details = ClientDetails.objects.get(session_id=session_id)

        client_id = details.pid 
        account_name = details.account_name
        branch = details.branch
        fullname = details.fullname  

        base_currency = "False" 
        url = "https://openexchangerates.org/api/currencies.json?prettyprint=false&show_alternative=false&show_inactive=false&app_id=usd"

        headers = {"accept": "application/json"}

        dineros = requests.get(url, headers=headers).json()


        try:
            all_currencies = Currency.objects.filter(client_id=client_id, base=True)

            if len(all_currencies) > 0:
                base_currency = "True"
        except:
            base_currency = "False"        

    
        if request.method == 'POST':
            currencies = request.POST.get('currency')
            base = request.POST.get('base')

            currency = Currency(currency=currencies, client_id=client_id, client=fullname)
            currency.save()

            if base == "base":
                currency.base = True
                currency.save()

            activity = ActivityLog(user=fullname, branch=branch, client_id=client_id, action=f'created currency {currencies}')    
            activity.save()
                
            messages.success(request, 'Currency created successfully!')
            return redirect('superuser:viewCurrency')


        else:
            return render(request, template_name, {
                'base_currency': base_currency,
                'data':dineros,
                'pid': client_id,
                'branch':branch,
                'account_name':account_name,
                'session_id':session_id,
                
            })    




# View currency

def viewCurrency(request, **kwargs):

    template_name = 'superuser/view-currency.html'

    
    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
 
    account_name = details.account_name
    branch = details.branch
    unlimited = details.unlimited
 
    currencies = Currency.objects.filter(client_id=client_id)

    return render(request, template_name, {
        'currencies': currencies,
        'pid': client_id,
        'branch':branch,
        'account_name':account_name, 
        'session_id':session_id, 
        'unlimited': unlimited,       
    })





# Edit Currency
def editCurrency(request, id, **kwargs):


    template_name = 'superuser/edit-currency.html'

    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
 
    account_name = details.account_name
    branch = details.branch
    fullname = details.fullname      


    url = "https://openexchangerates.org/api/currencies.json?prettyprint=false&show_alternative=false&show_inactive=false&app_id=usd"

    headers = {"accept": "application/json"}

    dineros = requests.get(url, headers=headers).json()

    currency = Currency.objects.get(id=id)

    try:
        existing_base = Currency.objects.get(client_id=client_id, base=True)
    
        if request.method == 'POST':
            currency.currency = request.POST.get('currency')
            base = request.POST.get('base')

            if base == "base":
                currency.base = True
                existing_base.base = False
            else: 
                currency.base = False
                existing_base.base = True   


            existing_base.save()
            currency.save()

            activity = ActivityLog(user=fullname, branch=branch, client_id=client_id, action=f'edited currency {currency}')    
            activity.save()

            messages.success(request, 'Currrency editted successfully!')
            return redirect('superuser:viewCurrency')  

    except:
    
        if request.method == 'POST':
            currency.currency = request.POST.get('currency')
            base = request.POST.get('base')

            if base == "base":
                currency.base = True
            else: 
                currency.base = False


            currency.save()

            activity = ActivityLog(user=fullname, branch=branch, client_id=client_id, action=f'edited currency {currency}')    
            activity.save()

            messages.success(request, 'Currrency editted successfully!')
            return redirect('superuser:viewCurrency')          


    return render(request, template_name, {
        'currency': currency,
        'data':dineros,
        'pid': client_id,
        'branch':branch,
        'account_name':account_name,
        'session_id':session_id,     
    }) 





# Delete Currency
def deleteCurrency(request, id, *args, **kwargs):

    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    branch = details.branch
    fullname = details.fullname  

    if request.method == "POST":
        currency = Currency.objects.get(id=id)
        currency.delete()

        activity = ActivityLog(user=fullname, branch=branch, client_id=client_id, action=f'deleted currency {currency}')    
        activity.save()
        messages.success(request, 'Currency deleted successfully!')
        return redirect('superuser:viewCurrency')






# Invoice
def createInvoice(request, **kwargs):

    template_name = 'superuser/create-invoice.html'

    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch
    fullname = details.fullname


    payload = json.dumps({ "phone_email": email, "password": password, "checkDeviceInfo": False })

    headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=Ly8oYWb8c70C2CDUYfFd0poVjCL91Octs99w3q6rGjSu8L2SaPVDoGPvJ4tKQIda; sessionid=4zyr1pvz9r6hyu8sqvuh0gqqxsymo56n'
    }

   
    branch_url = "https://db-api-v2.akwaabasoftware.com/clients/branch"
    branches = requests.request("GET", branch_url, headers=headers, data=payload).json()['data']


    member_category_url = "https://db-api-v2.akwaabasoftware.com/members/groupings/member-category"
    member_categories = requests.request("GET", member_category_url, headers=headers, data=payload).json()['data']


    if request.method == 'POST': 
        all_sectors = request.POST.get('all_sectors')
        member_type = request.POST.get('member_type')

        member_category_id = request.POST.get('member_category')

        member_category_url = f"https://db-api-v2.akwaabasoftware.com/members/groupings/member-category/{member_category_id}"
        member_category = requests.request("GET", member_category_url, headers=headers, data=payload).json()['data']['category']

        fee_type_id = request.POST.get('fee_type')
        fee_type = FeeType.objects.get(id=fee_type_id)   


        fee_description_id = request.POST.get('fee_description')
        fee_description = FeeDescription.objects.get(id=fee_description_id)

        invoice_type = request.POST.get('invoice_type')
    

        items = request.POST.getlist('items_amount[]')
        total_amount = 0
        total_amounts = 0

        string_items = [x for x in items if x != ""]
        str1 = [int(x) for x in string_items]
        items_amount = ','.join(str(e) for e in str1)
        for i in str1:
            total_amount += i


        info = []

        if all_sectors == "all_branches":

            branches = requests.request("GET", branch_url, headers=headers, data=payload).json()['data']

            for x in branches:

                url = f"https://db-api-v2.akwaabasoftware.com/members/groupings/group?branchId={x['id']}"
                    
                groups = requests.request("GET", url, headers=headers, data=payload).json()['data']


                if groups == []:

                    data = {
                        'branch_id': x['id'],
                        'branch': x['name'],
                        'group_id': "None",
                        'group': "None",
                        'subgroup_id': "None",
                        'subgroup': "None",
                    }

                    info.append(data)
                    
                 
                else:
                    for y in groups:
                        
                        url = f"https://db-api-v2.akwaabasoftware.com/members/groupings/sub-group?datatable_plugin&groupId={y['id']}"

                        subgroups = requests.request("GET", url, headers=headers, data=payload).json()['data']


                        if subgroups == []:

                            data = {
                                'branch_id': x['id'],
                                'branch': x['name'],
                                'group_id': y['id'],
                                'group': y['group'],
                                'subgroup_id': "None",
                                'subgroup': "None",
                            }

                            info.append(data)
                                
                        
                        else:
                            for z in subgroups:

                                data = {
                                'branch_id': x['id'],
                                'branch': x['name'],
                                'group_id': y['id'],
                                'group': y['group'],
                                'subgroup_id': z['id'],
                                'subgroup': z['subgroup'],
                                }

                                info.append(data)

    

            for x in range(len(info)):

                invoice = Invoice.objects.create(
                    branch_id = info[x]['branch_id'],
                    branch = info[x]['branch'],

                    group_id = info[x]['group_id'],
                    group = info[x]['group'],

                    subgroup_id = info[x]['subgroup_id'],
                    subgroup = info[x]['subgroup'],

                    member_category_id=member_category_id,
                    member_category=member_category, 
                    fee_type=fee_type,
                    fee_description= fee_description,
                    items_amount=items_amount, 
                    total_amount=total_amount, 
                    client_id=client_id, 
                    invoice_type=invoice_type,
                    client=fullname,
                    member_type=member_type,
                    )
                invoice.save()


                fee_items_names = [x.fee_items for x in FeeItems.objects.all()]
                fee_items_ids = []

                for x in fee_items_names:
                        fee_items_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print("pass")

                for i in fee_items_ids:
                    invoice.fee_items.add(FeeItems.objects.get(id=i))




        elif all_sectors == "all_groups":

            branch_id = request.POST.get('branch')

            payload = json.dumps({})

            headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json',
            'Cookie': 'csrftoken=yNDF0QM5CW2QBNy2NUMketfGhkwuR4jkCRaHylrYm1HRZ7AICGwYZ39CKkjzEXue; sessionid=7w7fqr0htni2s8f3koi883t715guq8kb'
            }

            branch_url = f"https://db-api-v2.akwaabasoftware.com/clients/branch/{branch_id}"
            try:
                branch = requests.request("GET", branch_url, headers=headers, data=payload).json()['data']['name']
            except:
                branch = "None" 


    
            url = f"https://db-api-v2.akwaabasoftware.com/members/groupings/group?branchId={branch_id}"
                
            groups = requests.request("GET", url, headers=headers, data=payload).json()['data']


            if groups == []:

                data = {
                    'branch_id': branch_id,
                    'branch': branch,
                    'group_id': "None",
                    'group': "None",
                    'subgroup_id': "None",
                    'subgroup': "None",
                }

                info.append(data)
                
                
            else:
                for y in groups:
                    
                    url = f"https://db-api-v2.akwaabasoftware.com/members/groupings/sub-group?datatable_plugin&groupId={y['id']}"

                    subgroups = requests.request("GET", url, headers=headers, data=payload).json()['data']


                    if subgroups == []:

                        data = {
                            'branch_id': branch_id,
                            'branch': branch,
                            'group_id': y['id'],
                            'group': y['group'],
                            'subgroup_id': "None",
                            'subgroup': "None",
                        }

                        info.append(data)
                            
                    
                    else:
                        for z in subgroups:

                            data = {
                            'branch_id': branch_id,
                            'branch': branch,
                            'group_id': y['id'],
                            'group': y['group'],
                            'subgroup_id': z['id'],
                            'subgroup': z['subgroup'],
                            }

                            info.append(data)

    
            for x in range(len(info)):
    
                invoice = Invoice.objects.create(
                    branch_id = info[x]['branch_id'],
                    branch = info[x]['branch'],

                    group_id = info[x]['group_id'],
                    group = info[x]['group'],

                    subgroup_id = info[x]['subgroup_id'],
                    subgroup = info[x]['subgroup'],

                    member_category_id=member_category_id,
                    member_category=member_category, 
                    fee_type=fee_type,
                    fee_description= fee_description,
                    items_amount=items_amount, 
                    total_amount=total_amount, 
                    client_id=client_id, 
                    invoice_type=invoice_type,
                    client=fullname,
                    member_type=member_type,
                    )
                invoice.save()


                fee_items_names = [x.fee_items for x in FeeItems.objects.all()]
                fee_items_ids = []

                for x in fee_items_names:
                        fee_items_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print("pass")

                for i in fee_items_ids:
                    invoice.fee_items.add(FeeItems.objects.get(id=i))



        elif all_sectors == "all_subgroups":
            
            branch_id = request.POST.get('branch')
            group_id = request.POST.get('group')

            payload = json.dumps({})

            headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json',
            'Cookie': 'csrftoken=yNDF0QM5CW2QBNy2NUMketfGhkwuR4jkCRaHylrYm1HRZ7AICGwYZ39CKkjzEXue; sessionid=7w7fqr0htni2s8f3koi883t715guq8kb'
            }


            branch_url = f"https://db-api-v2.akwaabasoftware.com/clients/branch/{branch_id}"
            try:
                branch = requests.request("GET", branch_url, headers=headers, data=payload).json()['data']['name']
            except:
                branch = "None" 

  

            group_url = f"https://db-api-v2.akwaabasoftware.com/members/groupings/group/{group_id}"
            
            try:
                group = requests.request("GET", group_url, headers=headers, data=payload).json()['data']['group']
            except:
                group = "None" 


                    
            url = f"https://db-api-v2.akwaabasoftware.com/members/groupings/sub-group?datatable_plugin&groupId={group_id}"

            subgroups = requests.request("GET", url, headers=headers, data=payload).json()['data']


            if subgroups == []:

                data = {
                    'branch_id': branch_id,
                    'branch': branch,
                    'group_id': group_id,
                    'group': group,
                    'subgroup_id': "None",
                    'subgroup': "None",
                }

                info.append(data)
                    
            
            else:
                for z in subgroups:

                    data = {
                    'branch_id': branch_id,
                    'branch': branch,
                    'group_id': group_id,
                    'group': group,
                    'subgroup_id': z['id'],
                    'subgroup': z['subgroup'],
                    }

                    info.append(data)

    
            for x in range(len(info)):
    
                invoice = Invoice.objects.create(
                    branch_id = info[x]['branch_id'],
                    branch = info[x]['branch'],

                    group_id = info[x]['group_id'],
                    group = info[x]['group'],

                    subgroup_id = info[x]['subgroup_id'],
                    subgroup = info[x]['subgroup'],

                    member_category_id=member_category_id,
                    member_category=member_category, 
                    fee_type=fee_type,
                    fee_description= fee_description,
                    items_amount=items_amount, 
                    total_amount=total_amount, 
                    client_id=client_id, 
                    invoice_type=invoice_type,
                    client=fullname,
                    member_type=member_type,
                    )
                invoice.save()


                fee_items_names = [x.fee_items for x in FeeItems.objects.all()]
                fee_items_ids = []

                for x in fee_items_names:
                        fee_items_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print("pass")

                for i in fee_items_ids:
                    invoice.fee_items.add(FeeItems.objects.get(id=i))




        else:

            branch_id = request.POST.get('branch')
            group_id = request.POST.get('group')
            subgroup_id = request.POST.get('subgroup', None)



            payload = json.dumps({})

            headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json',
            'Cookie': 'csrftoken=yNDF0QM5CW2QBNy2NUMketfGhkwuR4jkCRaHylrYm1HRZ7AICGwYZ39CKkjzEXue; sessionid=7w7fqr0htni2s8f3koi883t715guq8kb'
            }

            branch_url = f"https://db-api-v2.akwaabasoftware.com/clients/branch/{branch_id}"
            try:
                branch = requests.request("GET", branch_url, headers=headers, data=payload).json()['data']['name']
            except:
                branch = "None" 

        

            group_url = f"https://db-api-v2.akwaabasoftware.com/members/groupings/group/{group_id}"
            
            try:
                group = requests.request("GET", group_url, headers=headers, data=payload).json()['data']['group']
            except:
                group = "None" 


            subgroup_url = f"https://db-api-v2.akwaabasoftware.com/members/groupings/sub-group/{subgroup_id}"
            try:
                subgroup = requests.request("GET", subgroup_url, headers=headers, data=payload).json()['data']['subgroup']
            except:
                subgroup = "None"    



            invoice = Invoice.objects.create(
                
                branch_id = branch_id,
                branch = branch,
                group_id = group_id,
                group = group,
                subgroup_id = subgroup_id,
                subgroup = subgroup,
                member_category_id=member_category_id,
                member_category=member_category, 
                fee_type=fee_type,
                fee_description= fee_description,
                items_amount=items_amount, 
                total_amount=total_amount, 
                client_id=client_id, 
                invoice_type=invoice_type,
                client=fullname,
                member_type=member_type,
                )
            invoice.save()


            fee_items_names = [x.fee_items for x in FeeItems.objects.all()]
            fee_items_ids = []

            for x in fee_items_names:
                    fee_items_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print("pass")

            for i in fee_items_ids:
                invoice.fee_items.add(FeeItems.objects.get(id=i))



        
            
        activity = ActivityLog(user=fullname, branch=branch, client_id=client_id, action=f'created an invoice with id {invoice.id}')    
        activity.save()
        messages.success(request, 'Invoice created successfully!')
        return redirect('superuser:viewInvoice')

    else:
        return render(request, template_name, {
            'fee_type': FeeType.objects.filter(client_id=client_id),
            'fee_items': FeeItems.objects.filter(client_id=client_id),
            'fee_description': FeeDescription.objects.filter(client_id=client_id),
            'member_categories': member_categories,
            'branches':branches,
            'pid': client_id,
            'branch':branch,
            'account_name':account_name, 
            'session_id':session_id,
        }) 







# Edit invoice
def editInvoice(request, id, **kwargs):

    template_name = 'superuser/edit-invoice.html'
    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch
    fullname = details.fullname  


    payload = json.dumps({ "phone_email": email, "password": password, "checkDeviceInfo": False })

    headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=Ly8oYWb8c70C2CDUYfFd0poVjCL91Octs99w3q6rGjSu8L2SaPVDoGPvJ4tKQIda; sessionid=4zyr1pvz9r6hyu8sqvuh0gqqxsymo56n'
    }

   
    branch_url = "https://db-api-v2.akwaabasoftware.com/clients/branch"
    branches = requests.request("GET", branch_url, headers=headers, data=payload).json()['data']


    member_category_url = "https://db-api-v2.akwaabasoftware.com/members/groupings/member-category"
    member_categories = requests.request("GET", member_category_url, headers=headers, data=payload).json()['data']
    
    # print(member_categories)

    invoice = Invoice.objects.get(id=id)

    stuff = [(invoice.fee_items) for invoice in invoice.fee_items.all()]
    item_amount = (invoice.items_amount).split(',')


    data = dict(zip(stuff, item_amount))


    if request.method == 'POST':

        branch_id = request.POST.get('branch')
        member_category_id = request.POST.get('member_category')

        group_id = request.POST.get('group')
        subgroup_id = request.POST.get('subgroup', None)
        


        branch_url = f"https://db-api-v2.akwaabasoftware.com/clients/branch/{branch_id}"
        try:
            branch = requests.request("GET", branch_url, headers=headers, data=payload).json()['data']['name']
        except:
            branch = "None" 

       

        member_category_url = f"https://db-api-v2.akwaabasoftware.com/members/groupings/member-category/{member_category_id}"
        member_category = requests.request("GET", member_category_url, headers=headers, data=payload).json()['data']['category']



   
        if type(group_id) == int:

            group_url = f"https://db-api-v2.akwaabasoftware.com/members/groupings/group/{group_id}"
            

            try:
                group = requests.request("GET", group_url, headers=headers, data=payload).json()['data']['group']
            except:
                group = "None" 

        else:
            group = group_id         




        if type(subgroup_id) == int:

            subgroup_url = f"https://db-api-v2.akwaabasoftware.com/members/groupings/sub-group/{subgroup_id}"
            try:
                subgroup = requests.request("GET", subgroup_url, headers=headers, data=payload).json()['data']['subgroup']
            except:
                subgroup = "None"    

        else:
            subgroup = subgroup_id          




        invoice.branch = branch
        invoice.member_category = member_category
        invoice.group = group
        invoice.subgroup = subgroup


        invoice.invoice_type = request.POST.get('invoice_type')
        invoice.member_type = request.POST.get('member_type')


        # fee_type = request.POST.get('fee_type')
        fee_type_id = request.POST.get('fee_type')
        invoice.fee_type = FeeType.objects.get(id=fee_type_id)   

        fee_description_id = request.POST.get('fee_description')
        invoice.fee_description = FeeDescription.objects.get(id=fee_description_id)


        items = request.POST.getlist('items_amount[]')
        invoice.total_amount = 0

        string_items = [x for x in items if x != ""]
        str1 = [int(x) for x in string_items]

        invoice.items_amount = ','.join(str(e) for e in str1)
        for i in str1:
            invoice.total_amount += i

        invoice.save()


        fee_items_names = [x.fee_items for x in FeeItems.objects.all()]
        fee_items_ids = []

        for x in fee_items_names:
                fee_items_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print("pass")

        for i in fee_items_ids:
            invoice.fee_items.add(FeeItems.objects.get(id=i))

        activity = ActivityLog(user=fullname, branch=branch, client_id=client_id, action=f'edited an invoice with id {invoice.id}')    
        activity.save()

        messages.success(request, 'Invoice edited successfully!')
        return redirect('superuser:viewInvoice')



    return render(request, template_name, {
        'invoice': invoice,
        'stuff': stuff,
        'item_amount': item_amount,
        'data': data,
        'fee_types': FeeType.objects.all(),
        'fee_items': FeeItems.objects.all(),
        'fee_descriptions': FeeDescription.objects.filter(client_id=client_id),          

        'pid': client_id,
        'branch':branch,
        'account_name':account_name, 
        'branches': branches,
        'member_categories': member_categories,
        'session_id':session_id,
        # 'groups': groups,
        # 'subgroups': subgroups,
    }) 





def load_items(request):
    template_name = 'superuser/test.html'

    if request.method == 'GET': 
        fee_type = request.GET.get('fee_type')
        fee_items = FeeItems.objects.filter(fee_type=fee_type).order_by('fee_type')
        return render(request, template_name, {'fee_items': fee_items})






def load_groups(request):
    template_name = 'superuser/groups.html'

    if request.method == 'GET': 

        session_id = request.COOKIES.get('session_id')
        details = ClientDetails.objects.get(session_id=session_id)

        client_id = details.pid
        token = details.token
        email = details.email  
        password = details.password  
        account_name = details.account_name
        branch = details.branch
        fullname = details.fullname 


        branch = request.GET.get('branch')
        pid = request.GET.get('pid')
 

        url = f"https://db-api-v2.akwaabasoftware.com/members/groupings/group?branchId={branch}"

        payload = json.dumps({})

        headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=yNDF0QM5CW2QBNy2NUMketfGhkwuR4jkCRaHylrYm1HRZ7AICGwYZ39CKkjzEXue; sessionid=7w7fqr0htni2s8f3koi883t715guq8kb'
        }

        groups = requests.request("GET", url, headers=headers, data=payload).json()['data']

        return render(request, template_name, {'groups': groups})



def load_subgroups(request):
    template_name = 'superuser/subgroups.html'
    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
 

    
    if request.method == 'GET': 
        group = request.GET.get('group')
        pid = request.GET.get('pid')
 

        url = f"https://db-api-v2.akwaabasoftware.com/members/groupings/sub-group?datatable_plugin&groupId={group}"

        payload = json.dumps({})

        headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=yNDF0QM5CW2QBNy2NUMketfGhkwuR4jkCRaHylrYm1HRZ7AICGwYZ39CKkjzEXue; sessionid=7w7fqr0htni2s8f3koi883t715guq8kb'
        }

        subgroups = requests.request("GET", url, headers=headers, data=payload).json()['data']

        return render(request, template_name, {'subgroups': subgroups})





         
# View invoice

def viewInvoice(request, **kwargs):

    template_name = 'superuser/view-invoice.html'

    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid

    account_name = details.account_name
    branch = details.branch
    
    unlimited = details.unlimited  

    invoices = Invoice.objects.filter(client_id=client_id)
 

    if request.method == 'GET':
        my_filter = InvoicesFilter(request.GET, queryset=invoices)
        all_invoices = my_filter.qs


    return render(request, template_name, {
        'my_filter': my_filter,
        'invoices': all_invoices,
        'pid': client_id,
        'branch':branch,
        'account_name':account_name, 
        'session_id':session_id,  
        'unlimited': unlimited,      
    }) 

    






# Create Invoice Details
def setInvoiceDetails(request, **kwargs):
    template_name = 'superuser/set-invoice.html'

    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    email = details.email  
    account_name = details.account_name
    branch = details.branch
    fullname = details.fullname  


    if request.method == "POST":
        signers_name = request.POST.get('signers_name')
        company_name = request.POST.get('company_name')
        signature = request.FILES.get('signature')
        logo = request.FILES.get('logo')
        contact = request.POST.get('contact')
        email = request.POST.get('email')

        postal_address = request.POST.get('other_contact')
        digital_address = request.POST.get('digital_address')

        website = request.POST.get('website')
        website = f'https://{website}'

        location = request.POST.get('location')

        whatsapp = request.POST.get('whatsapp')
        whatsapp = f'233{int(whatsapp)}'

        telegram = request.POST.get('telegram')
        telegram = f'233{int(telegram)}'

        facebook = request.POST.get('facebook')
        twitter = request.POST.get('twitter')
        instagram = request.POST.get('instagram')
        about = request.POST.get('about')
        services = request.POST.get('services')


        invoice_details = InvoiceDetails(
            client_id=client_id, 
            client=fullname, 
            signers_name=signers_name, 
            company_name=company_name, 
            signature=signature, 
            logo=logo, 
            contact=contact, 
            email=email,
            postal_address=postal_address,
            digital_address=digital_address,
            website=website,
            location=location,
            whatsapp=whatsapp,
            telegram=telegram,
            facebook=facebook,
            twitter=twitter,
            instagram=instagram,
            about=about,
            services=services,
        )
        invoice_details.save()

        activity = ActivityLog(user=fullname, branch=branch, client_id=client_id, action=f'set organization details')    
        activity.save()

        messages.success(request, 'Receipt details set successfully!')

        # return HttpResponseRedirect(reverse('superuser:viewInvoiceDetails'))
        return redirect('superuser:viewInvoiceDetails') 
        # return HttpResponseRedirect('/view-invoice-details')
    else:
        return render(request, template_name, {
            'pid': client_id,
            'session_id':session_id,
            'branch':branch,
            'account_name':account_name,             
        })    





# View Invoice Details
def viewInvoiceDetails(request, **kwargs):

    template_name = 'superuser/view-invoice-details.html'

    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
 
    account_name = details.account_name
    branch = details.branch

    unlimited = details.unlimited  


    return render(request, template_name, {
        'invoice_details': InvoiceDetails.objects.filter(client_id=client_id),
        'pid': client_id,
        'branch':branch,
        'account_name':account_name,
        'session_id':session_id,  
        'unlimited': unlimited,       
    })







# Edit invoice details
def editInvoiceDetails(request, id, **kwargs):
    # if ClientDetails.objects.count() > 0:

    template_name = 'superuser/edit-invoice-details.html'
    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    account_name = details.account_name
    branch = details.branch
    fullname = details.fullname      

    invoice_detail = InvoiceDetails.objects.get(id=id)
    
    if request.method == 'POST':
        new_signature = request.FILES.get('signature', None)
        if new_signature is not None:
            invoice_detail.signature = request.FILES.get('signature', None)

        new_logo = request.FILES.get('logo', None)
        if new_logo is not None:
            invoice_detail.logo = request.FILES.get('logo', None)

        invoice_detail.signers_name = request.POST.get('signers_name')
        invoice_detail.company_name = request.POST.get('company_name')
        invoice_detail.contact = request.POST.get('contact')
        invoice_detail.email = request.POST.get('email')

        invoice_detail.postal_address = request.POST.get('postal_address')
        invoice_detail.digital_address = request.POST.get('digital_address')
        invoice_detail.website = request.POST.get('website')
        invoice_detail.location = request.POST.get('location')
        invoice_detail.whatsapp = request.POST.get('whatsapp')
        invoice_detail.telegram = request.POST.get('telegram')
        invoice_detail.facebook = request.POST.get('facebook')
        invoice_detail.twitter = request.POST.get('twitter')
        invoice_detail.instagram = request.POST.get('instagram')
        invoice_detail.about = request.POST.get('about')
        invoice_detail.services = request.POST.get('services')
    

        invoice_detail.save() 

        activity = ActivityLog(user=fullname, branch=branch, client_id=client_id, action=f'edited organization details')    
        activity.save() 

        messages.success(request, 'Receipt details edited successfully!')
        return redirect('superuser:viewInvoiceDetails') 
        # return HttpResponseRedirect(reverse('superuser:viewInvoiceDetails')) 
        # return HttpResponseRedirect('/view-invoice-details')

    return render(request, template_name, {
        'invoice_detail': invoice_detail,
        'pid': client_id,
        'branch':branch,
        'account_name':account_name,
        'session_id':session_id, 
    }) 

    # else:
    #     messages.error(request, 'Please Login to continue') 
    #     return HttpResponseRedirect(reverse('login:login'))



# Delete Invoice Details
def deleteInvoiceDetails(request, id, *args, **kwargs):

    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid

    branch = details.branch
    fullname = details.fullname   


    if request.method == "POST":
        invoice_detail = InvoiceDetails.objects.get(id=id)
        invoice_detail.delete()

        activity = ActivityLog(user=fullname, branch=branch, client_id=client_id, action=f'deleted organization details')    
        activity.save() 
        messages.success(request, 'Receipt details deleted successfully!')

        return redirect('superuser:viewInvoiceDetails') 




# Auto assign
def assignPaymentsDuration(request, **kwargs):


    template_name = 'superuser/assign-payments.html'
    pk = kwargs.get('pk')
    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    account_name = details.account_name
    branch = details.branch
    fullname = details.fullname      


    invoice = get_object_or_404(Invoice, pk=pk)
    today = datetime.datetime.now()
    year = datetime.datetime.now().year
    year = str(year) + "0000"


    try:
        company_name = InvoiceDetails.objects.filter(client_id=client_id).first().company_name
    except:
        company_name = "Client Service Alert"




    payload = json.dumps({})

    headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=yNDF0QM5CW2QBNy2NUMketfGhkwuR4jkCRaHylrYm1HRZ7AICGwYZ39CKkjzEXue; sessionid=7w7fqr0htni2s8f3koi883t715guq8kb'
    }


    try:
        email_url = f'https://super.akwaabasoftware.com/api/client-email/{client_id}/'
        client_email = requests.request("GET", email_url, headers=headers, data=payload).json()['email']    
        client_password = requests.request("GET", email_url, headers=headers, data=payload).json()['password'] 

        EMAIL_BACKEND = env('EMAIL_BACKEND')
        EMAIL_HOST = env('EMAIL_HOST')
        EMAIL_USE_TLS = env('EMAIL_USE_TLS')
        EMAIL_PORT = env('EMAIL_PORT')
        EMAIL_HOST_USER = client_email
        EMAIL_HOST_PASSWORD = client_password

    except:

        EMAIL_BACKEND = env('EMAIL_BACKEND')
        EMAIL_HOST = env('EMAIL_HOST')
        EMAIL_USE_TLS = env('EMAIL_USE_TLS')
        EMAIL_PORT = env('EMAIL_PORT')
        EMAIL_HOST_USER = env('EMAIL_HOST_USER')
        EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
      



    
    if invoice.member_type == 'individual':
        # all_url = f"https://db-api-v2.akwaabasoftware.com/members/groupings/sub-group-member?datatable_plugin&branchId={invoice.branch_id}&memberCategoryId={invoice.member_category_id}&groupId={invoice.group_id}&subgroupId={invoice.subgroup_id}"
        all_url = f"https://db-api-v2.akwaabasoftware.com/members/user?datatable_plugin&length=1000&branchId={invoice.branch_id}&memberType={invoice.member_category_id}&groupId={invoice.group_id}&subgroupId={invoice.subgroup_id}"
        try:
            response = requests.request("GET", all_url, headers=headers, data=payload).json()['data']
            answer = [] 
        except:
            response = []   
            answer = [] 
    

    else:

        org_url = f"https://db-api-v2.akwaabasoftware.com/members/user-organization?datatable_plugin&branchId={invoice.branch_id}&memberType={invoice.member_category_id}&groupId={invoice.group_id}&subgroupId={invoice.subgroup_id}"

        try:
            answer = requests.request("GET", org_url, headers=headers, data=payload).json()['data']
            response = [] 
        except:
            answer = [] 
            response = [] 
   

 

    if request.method == 'POST':
        branch = request.POST.get('branch')
        member_category = request.POST.get('member_category')
        group = request.POST.get('group')
        subgroup = request.POST.get('subgroup')

        try:
            member = request.POST.get('member')
        except:
            member = ""


        invoice_type = request.POST.get('invoice_type')
        member_type = request.POST.get('member_type')

        # fee_type = request.POST.get('fee_type')
        fee_type_id = request.POST.get('fee_type')
        fee_type = FeeType.objects.get(id=fee_type_id) 

        fee_description_id = request.POST.get('fee_description')
        fee_description = FeeDescription.objects.get(id=fee_description_id) 



        promo = request.POST.get('promo')

        if promo == "promo":
            total_invoice = request.POST.get('discounted_amount')
            expiration_bill = request.POST.get('discounted_amount')
        else:
            total_invoice = request.POST.get('total_invoice')
            expiration_bill = request.POST.get('total_invoice')




        install_range = request.POST.get('install_range')



        if install_range == 'Day(s)':

            end_date =  request.POST.get('set_pay_date')
            pay_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y/%m/%d')
            begin_date = datetime.datetime.today().strftime('%Y/%m/%d')
            
            num1= datetime.datetime.strptime(pay_date, "%Y/%m/%d")
            num2= datetime.datetime.strptime(begin_date, "%Y/%m/%d")
            
            install_period =  (num1 - num2).days
            amount_by_days =  round(int(total_invoice) / (int(install_period)))




        elif install_range == 'Month(s)': 

            start_date =  request.POST.get('start_date')
            end_date =  request.POST.get('end_date')

            begin_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y/%m/%d')
            pay_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y/%m/%d')
            
            num1= datetime.datetime.strptime(pay_date, "%Y/%m/%d")
            num2= datetime.datetime.strptime(begin_date, "%Y/%m/%d")
            
            install_period =  (num1 - num2).days
            amount_by_days =  round(int(total_invoice) / (int(install_period)))



        elif install_range == 'Year(s)': 
            no_of_years = request.POST.get('no_of_years') 

            install_period = int(no_of_years) * 365

            end_date =  today + datetime.timedelta(days=(int(install_period)))
            amount_by_days =  round(int(total_invoice) / (int(install_period)))

        else:
            install_period = None
            end_date = None
            amount_by_days = None





        # elif install_range == 'Month(s)':  
        #     start_date =  request.POST.get('start_date')
        #     end_date =  request.POST.get('end_date')
        #     amount_by_days =  round(int(total_invoice) / (int(install_period) * 30))
        #     # subscription_expiry =  today + datetime.timedelta(days=(int(install_period) * 30))

        # elif install_range == 'Year(s)':    
        #     amount_by_days =  round(int(total_invoice) / (int(install_period) * 365))
        #     end_date =  today + datetime.timedelta(days=(int(install_period) * 365))






        all_members = request.POST.get('all_members')
        expiry = request.POST.get('deactivate')


        # if assigned.deactivate == "True":
        #     if install_range == 'Day(s)':
        #             subscription_expiry =  today + datetime.timedelta(days=(int(install_period)))
        #     elif install_range == 'Month(s)':  
        #         subscription_expiry =  today + datetime.timedelta(days=(int(install_period) * 30))
        #     elif install_range == 'Year(s)':    
        #         subscription_expiry =  today + datetime.timedelta(days=(int(install_period) * 365))
        #     else:
        #         subscription_expiry = end_date 
        # else:
        #     subscription_expiry = None 


        # if install_range == 'Day(s)':
        #         amount_by_days =  round(int(total_invoice) / (int(install_period)))
        #         end_date =  today + datetime.timedelta(days=(int(install_period)))

        # elif install_range == 'Month(s)':  
        #     start_date =  request.POST.get('start_date')
        #     end_date =  request.POST.get('end_date')
        #     amount_by_days =  round(int(total_invoice) / (int(install_period) * 30))
        #     # subscription_expiry =  today + datetime.timedelta(days=(int(install_period) * 30))

        # elif install_range == 'Year(s)':    
        #     amount_by_days =  round(int(total_invoice) / (int(install_period) * 365))
        #     end_date =  today + datetime.timedelta(days=(int(install_period) * 365))


        # elif install_range == 'None':
        #     set_pay_date =  request.POST.get('set_pay_date')
        #     pay_date = datetime.datetime.strptime(set_pay_date, '%Y-%m-%d').strftime('%Y/%m/%d')
        #     begin_date = datetime.datetime.today().strftime('%Y/%m/%d')
            
        #     # datetime.datetime.today().strftime("%Y-%m-%d")

        #     num1= datetime.datetime.strptime(pay_date, "%Y/%m/%d")
        #     num2= datetime.datetime.strptime(begin_date, "%Y/%m/%d")
            
        #     dayss =  (num1 - num2).days
        #     amount_by_days =  round(int(total_invoice) / (int(dayss)))
        #     end_date =  set_pay_date





        if expiry == "deactivate":
            deactivate = True
        else:
            deactivate = False


        if all_members == "all_members":

            if member_type == 'individual':
                    
                for x in response:

                    firstname = x['firstname']
                    middlename = x['middlename']
                    surname = x['surname']
                    member_id = x['id']
                    email = x['email']
                    contact = x['phone']
                    # status = x['memberInfo']['status']

                    if middlename == "":
                        username = f"{firstname} {surname}"
                    else:
                        username = f"{firstname} {middlename} {surname}"   
                    
                    try:
                        usercode = Usercode.objects.get(member_id=member_id).usercode
                    except:
                        code = random.randint(10000, 99999)
                        chars = random_char(3)
                        usercode = f'{chars}{code}'

                        try:
                            existing_code = Usercode.objects.get(usercode=usercode).usercode

                            while True:
                                if usercode == existing_code:
                                    code = random.randint(10000, 99999)
                                    chars = random_char(3)
                                    usercode = f'{chars}{code}'
                                else:
                                    break    
    
                        except:
                            print("Something happened!")

                        membercode = Usercode.objects.create(member_id=member_id, member=username, client_id=client_id, usercode=usercode)  
                        membercode.save()  



                    try:
                        assignPayments = AssignPaymentDuration.objects.get(
                                    branch = branch,
                                    member_category = member_category,
                                    group = group,
                                    subgroup = subgroup,
                                    client_id = client_id,
                                    member_id = member_id,
                                    fee_type = fee_type,
                                    fee_description = fee_description,
                                    invoice_type=invoice_type,
                                                           
                            )

                    except:

                        assignPayments = AssignPaymentDuration.objects.create(
                                    branch = branch,
                                    member_category = member_category,
                                    group = group,
                                    subgroup = subgroup,
                                    member = username,
                                    client_id = client_id,
                                    member_id = member_id,
                                    usercode=usercode,
                                    fee_type = fee_type,
                                    fee_description = fee_description,
                                    total_invoice = total_invoice,
                                    expiration_bill=expiration_bill,
                                    install_range = install_range,
                                    install_period = install_period,
                                    end_date = end_date,
                                    amount_by_days=amount_by_days,
                                    invoice_type=invoice_type,
                                    deactivate=deactivate,                        
                        )

                        assignPayments.save()

            


                        total = TotalAmount(member=username, member_id=member_id, client_id=client_id, total= total_invoice, branch=branch, member_category=member_category, group=group, subgroup=subgroup)
                        total.save()


                        # Send email
                        subject = f'ASSIGNED BILL/INVOICE'
                        body = f"""
                                    Your new or updated invoice/bill from {company_name}. 
                                    Go to https://unaapp.org/ and sign up to get an ACCESS CODE 
                                    or login if you already have an access code for payment.
                                    Many thanks from {company_name}.
                                """
                        senders_mail = EMAIL_HOST_USER
                        to_address = [f'{email}']


                        # send_mail(subject, body, senders_mail, to_address, fail_silently=False)
                        # html_template = 'superuser/user_printer.html'

                        # html_message = render_to_string(html_template)

                        email = EmailMessage(subject, body, senders_mail, to_address)

                        try:
                            email.send()
                        except: 
                            print("Server error")
                            pass



                        # # Send SMS
                        private_key = env('PRIVATE_KEY')
                        public_key = env('PUBLIC_KEY')

                        if contact.startswith('0'):
                            phone_number = int(contact.replace(' ', '')[1:])
                            contact = f'233{phone_number}'


                        body = f"""
                                    Your new or updated invoice/bill from {company_name}. 
                                    Go to https://unaapp.org/ and sign up to get an ACCESS CODE 
                                    or login if you already have an access code for payment.
                                    Many thanks from {company_name}.
                                """

                        url = f"https://api.msmpusher.net/v1/send?privatekey={private_key}&publickey={public_key}&sender=UNAGH&numbers={contact}&message={body}"

                        payload = {}
                        headers = {}

                        try:
                            response = requests.request("GET", url, headers=headers, data=payload).json()
                        except:
                            pass
            else:

                for y in answer:

                    username = y['organizationName']
                    member_id = y['id']
                    email = y['organizationEmail']
                    contact = y['organizationPhone']
                    
                    try:
                        usercode = Usercode.objects.get(member_id=member_id).usercode
                    except:
                        code = random.randint(10000, 99999)
                        chars = random_char(3)
                        usercode = f'{chars}{code}'

                        try:
                            existing_code = Usercode.objects.get(usercode=usercode).usercode

                            while True:
                                if usercode == existing_code:
                                    code = random.randint(10000, 99999)
                                    chars = random_char(3)
                                    usercode = f'{chars}{code}'
                                else:
                                    break    
    
                        except:
                            print("Something happened!")

                        membercode = Usercode.objects.create(member_id=member_id, member=username, client_id=client_id, usercode=usercode)  
                        membercode.save()   
                                  
            
                try:
                        assignPayments = AssignPaymentDuration.objects.get(
                                    branch = branch,
                                    member_category = member_category,
                                    group = group,
                                    subgroup = subgroup,
                                    client_id = client_id,
                                    member_id = member_id,
                                    fee_type = fee_type,
                                    fee_description = fee_description,
                                    invoice_type=invoice_type,
                                                        
                            )

                except:            

                    assignPayments = AssignPaymentDuration(
                                    branch = branch,
                                    member_category = member_category,
                                    group = group,
                                    subgroup = subgroup,
                                    member = username,
                                    client_id = client_id,
                                    member_id = member_id,
                                    usercode=usercode,
                                    fee_type = fee_type,
                                    fee_description = fee_description,
                                    total_invoice = total_invoice,
                                    expiration_bill=expiration_bill,
                                    install_range = install_range,
                                    install_period = install_period,
                                    end_date = end_date,
                                    amount_by_days=amount_by_days,
                                    invoice_type=invoice_type,
                                    deactivate=deactivate,                        
                    )

                    assignPayments.save()

            
                    # if status == 1:
                    #     assignPayments.account_status = "Subscriber"
                    # else:
                    #     assignPayments.account_status = "Non Subscriber"

                    # assignPayments.save()


                    total = TotalAmount(member=username, member_id=member_id, client_id=client_id, total= total_invoice, branch=branch, member_category=member_category, group=group, subgroup=subgroup)
                    total.save()


                    # Send email
                    subject = f'ASSIGNED BILL/INVOICE'
                    body = f"""
                                Your new or updated invoice/bill from {company_name}. 
                                Go to https://unaapp.org/ and sign up to get an ACCESS CODE 
                                or login if you already have an access code for payment.
                                Many thanks from {company_name}.
                            """
                    senders_mail = EMAIL_HOST_USER
                    to_address = [f'{email}']


                    # send_mail(subject, body, senders_mail, to_address, fail_silently=False)
                    # html_template = 'superuser/user_printer.html'

                    # html_message = render_to_string(html_template)

                    email = EmailMessage(subject, body, senders_mail, to_address)

                    try:
                        email.send()
                    except: 
                        print("Server error")
                        pass



                    # # Send SMS
                    private_key = env('PRIVATE_KEY')
                    public_key = env('PUBLIC_KEY')

                    if contact.startswith('0'):
                        phone_number = int(contact.replace(' ', '')[1:])
                        contact = f'233{phone_number}'


                    body = f"""
                                Your new or updated invoice/bill from {company_name}. 
                                Go to https://unaapp.org/ and sign up to get an ACCESS CODE 
                                or login if you already have an access code for payment.
                                Many thanks from {company_name}.
                            """

                    url = f"https://api.msmpusher.net/v1/send?privatekey={private_key}&publickey={public_key}&sender=UNAGH&numbers={contact}&message={body}"

                    payload = {}
                    headers = {}

                    try:
                        response = requests.request("GET", url, headers=headers, data=payload).json()
                    except:
                        pass


                activity = ActivityLog(user=fullname, branch=branch, action=f'assigned {fee_type} to all {member_category} in {branch}, {group}')    
                activity.save() 



        else:

            if member_type == 'individual':

                url = f"https://db-api-v2.akwaabasoftware.com/members/user/{member}"

                payload = json.dumps({})
                headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json','Cookie': 'csrftoken=MmSz4Xh2CHMcrgt1chJAlu27V1FZvTjL2KUbJ9nqbaQw3fsCIUeebhhdigNSyZI4; sessionid=qvjnfg4gj0wey2swhm50ws0sy2hnx0az'}

                person = requests.request("GET", url, headers=headers, data=payload).json()['data']


                firstname = person['firstname']
                middlename = person['middlename']
                surname = person['surname']
                member_id = person['id']
                email = person['email']
                contact = person['phone']
                # status = person['status']

                if middlename == "":
                    username = f"{firstname} {surname}"
                else:
                    username = f"{firstname} {middlename} {surname}" 


                try:
                    usercode = Usercode.objects.get(member_id=member_id).usercode
                except:
                    code = random.randint(10000, 99999)
                    chars = random_char(3)
                    usercode = f'{chars}{code}'

                    try:
                        existing_code = Usercode.objects.get(usercode=usercode).usercode

                        while True:
                            if usercode == existing_code:
                                code = random.randint(10000, 99999)
                                chars = random_char(3)
                                usercode = f'{chars}{code}'
                            else:
                                break    
    
                    except:
                        pass
                    

                    membercode = Usercode.objects.create(member_id=member_id, member=username, client_id=client_id, usercode=usercode)  
                    membercode.save()         
                
                try:
                        assignPayments = AssignPaymentDuration.objects.get(
                                    branch = branch,
                                    member_category = member_category,
                                    group = group,
                                    subgroup = subgroup,
                                    client_id = client_id,
                                    member_id = member_id,
                                    fee_type = fee_type,
                                    fee_description = fee_description,
                                    invoice_type=invoice_type,
                                                        
                            )
                except:        

                    assignPayments = AssignPaymentDuration(
                                        branch = branch,
                                        member_category = member_category,
                                        group = group,
                                        subgroup = subgroup,
                                        member = username,
                                        client_id = client_id,
                                        member_id = member_id,
                                        usercode=usercode,
                                        fee_type = fee_type,
                                        fee_description = fee_description,
                                        total_invoice = total_invoice,
                                        expiration_bill=expiration_bill,
                                        install_range = install_range,
                                        install_period = install_period,
                                        end_date = end_date,
                                        invoice_type=invoice_type,
                                        amount_by_days=amount_by_days,
                                    )

                    assignPayments.save()


                    # if status == 1:
                    #     assignPayments.account_status = "subscriber"
                    # else:
                    #     assignPayments.account_status = "non_subscriber"

                    # assignPayments.save()


                    total = TotalAmount(member=username, member_id=member_id, client_id=client_id, total=total_invoice)
                    total.save()
                    # print(f"Client id is {client_id}")

                    # Send email
                    subject = f'ASSIGNED BILL/INVOICE'
                    body = f"""
                                Your new or updated invoice/bill from {company_name}. 
                                Go to https://unaapp.org/ and sign up to get an Access Code 
                                or login if you already have an access code for payment.
                                Many thanks from {company_name}.
                            """
                    senders_mail = EMAIL_HOST_USER
                    to_address = [f'{email}']



                    email = EmailMessage(subject, body, senders_mail, to_address)
                    try:
                        email.send()
                    except: 
                        print("Server error")
                        pass



                    # # Send SMS
                    private_key = env('PRIVATE_KEY')
                    public_key = env('PUBLIC_KEY')

                    if contact.startswith('0'):
                        phone_number = int(contact.replace(' ', '')[1:])
                        contact = f'233{phone_number}'


                    body = f"""
                                Your new or updated invoice/bill from {company_name}. 
                                Go to https://unaapp.org/ and sign up to get an ACCESS CODE 
                                or login if you already have an access code for payment.
                                Many thanks from {company_name}.
                            """

                    url = f"https://api.msmpusher.net/v1/send?privatekey={private_key}&publickey={public_key}&sender=UNAGH&numbers={contact}&message={body}"

                    payload = {}
                    headers = {}

                    try:
                        response = requests.request("GET", url, headers=headers, data=payload).json()
                    except:
                        pass


                    activity = ActivityLog(user=fullname, branch=branch, action=f'assigned {fee_type} to {username}')    
                    activity.save() 


            else:

                url = f"https://db-api-v2.akwaabasoftware.com/members/user-organization/{member}"

                payload = json.dumps({})
                headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json','Cookie': 'csrftoken=MmSz4Xh2CHMcrgt1chJAlu27V1FZvTjL2KUbJ9nqbaQw3fsCIUeebhhdigNSyZI4; sessionid=qvjnfg4gj0wey2swhm50ws0sy2hnx0az'}

                person = requests.request("GET", url, headers=headers, data=payload).json()['data']

                username = person['organizationName']
                member_id = person['id']
                email = person['organizationEmail']
                contact = person['organizationPhone']
                # status = person['status']

                try:
                    usercode = Usercode.objects.get(member_id=member_id).usercode
                except:
                    code = random.randint(10000, 99999)
                    chars = random_char(3)
                    usercode = f'{chars}{code}'

                    try:
                        existing_code = Usercode.objects.get(usercode=usercode).usercode

                        while True:
                            if usercode == existing_code:
                                code = random.randint(10000, 99999)
                                chars = random_char(3)
                                usercode = f'{chars}{code}'
                            else:
                                break    
    
                    except:
                        pass
                    

                    membercode = Usercode.objects.create(member_id=member_id, member=username, client_id=client_id, usercode=usercode)  
                    membercode.save()         
                
                try:
                        assignPayments = AssignPaymentDuration.objects.get(
                                    branch = branch,
                                    member_category = member_category,
                                    group = group,
                                    subgroup = subgroup,
                                    client_id = client_id,
                                    member_id = member_id,
                                    fee_type = fee_type,
                                    fee_description = fee_description,
                                    invoice_type=invoice_type,
                                                        
                            )
                except:        
                    assignPayments = AssignPaymentDuration(
                                        branch = branch,
                                        member_category = member_category,
                                        group = group,
                                        subgroup = subgroup,
                                        member = username,
                                        client_id = client_id,
                                        member_id = member_id,
                                        usercode=usercode,
                                        fee_type = fee_type,
                                        fee_description = fee_description,
                                        total_invoice = total_invoice,
                                        expiration_bill=expiration_bill,
                                        install_range = install_range,
                                        install_period = install_period,
                                        end_date = end_date,
                                        invoice_type=invoice_type,
                                        amount_by_days=amount_by_days,
                                    )

                    assignPayments.save()



                    total = TotalAmount(member=username, member_id=member_id, client_id=client_id, total=total_invoice)
                    total.save()
                    # print(f"Client id is {client_id}")

                    # Send email
                    subject = f'ASSIGNED BILL/INVOICE'
                    body = f"""
                                Your new or updated invoice/bill from {company_name}. 
                                Go to https://unaapp.org/ and sign up to get an Access Code 
                                or login if you already have an access code for payment.
                                Many thanks from {company_name}.
                            """
                    senders_mail = EMAIL_HOST_USER
                    to_address = [f'{email}']



                    email = EmailMessage(subject, body, senders_mail, to_address)
                    try:
                        email.send()
                    except: 
                        print("Server error")
                        pass



                    # # Send SMS
                    private_key = env('PRIVATE_KEY')
                    public_key = env('PUBLIC_KEY')

                    if contact.startswith('0'):
                        phone_number = int(contact.replace(' ', '')[1:])
                        contact = f'233{phone_number}'


                    body = f"""
                                Your new or updated invoice/bill from {company_name}. 
                                Go to https://unaapp.org/ and sign up to get an ACCESS CODE 
                                or login if you already have an access code for payment.
                                Many thanks from {company_name}.
                            """

                    url = f"https://api.msmpusher.net/v1/send?privatekey={private_key}&publickey={public_key}&sender=UNAGH&numbers={contact}&message={body}"

                    payload = {}
                    headers = {}

                    try:
                        response = requests.request("GET", url, headers=headers, data=payload).json()
                    except:
                        pass


                    activity = ActivityLog(user=fullname, branch=branch, action=f'assigned {fee_type} to {username}')    
                    activity.save() 


                

        if len(PrinterInvoice.objects.filter(branch=invoice.branch, member_category=invoice.member_category, group=invoice.group, subgroup=invoice.subgroup, fee_type=invoice.fee_type, fee_description=invoice.fee_description, items_amount=invoice.items_amount, total_amount=invoice.total_amount)) > 0:
            pass
        else:
            printer_invoice = PrinterInvoice(branch=invoice.branch, member_category=invoice.member_category, group=invoice.group, subgroup=invoice.subgroup, fee_type=invoice.fee_type, fee_description=invoice.fee_description, items_amount=invoice.items_amount, total_amount=invoice.total_amount)
            printer_invoice.save()

            fee_items_ids = [x.id for x in invoice.fee_items.all()]

            for i in fee_items_ids:
                printer_invoice.fee_items.add(invoice.fee_items.get(id=i))           


        messages.success(request, 'Invoice assigned successfully!')

        # return HttpResponseRedirect(reverse('superuser:viewPaymentDuration'))
        return redirect('superuser:viewPaymentDuration')  
        # return HttpResponseRedirect('/view-payment-details')
    else:
        return render(request, template_name, {
            'invoice': invoice,
            'period': AssignPeriod.objects.all(),
            'response': response,
            'pid': client_id,
            'branch':branch,
            'account_name':account_name,   
            'answer': answer,   
            'session_id':session_id,       
        })   







def load_breakdown(request):
    template_name = 'superuser/breakdown.html'

    if request.method == 'GET':
        assigned_id = request.GET.get('assigned_id')
        
  
        detail = get_object_or_404(AssignPaymentDuration, pk=assigned_id)

        try:
            invoice = Invoice.objects.get(fee_type= detail.fee_type, branch= detail.branch, member_category= detail.member_category, group= detail.group, subgroup= detail.subgroup)
        except:
            try:
                invoice = PrinterInvoice.objects.get(fee_type= detail.fee_type, branch= detail.branch, member_category= detail.member_category, group= detail.group, subgroup= detail.subgroup, total_amount=detail.outstanding_bill)
            except:
                return HttpResponse("Invoice does not exist")    

        keys = [item.fee_items for item in invoice.fee_items.all()]
        values = ["{:,}".format(int(i)) for i in invoice.items_amount.split(',')]
        data = dict(zip(keys, values))


        return render(request, template_name, {
            'data': data
            })



def viewAccessCodes(request, **kwargs):
    template_name = 'superuser/access.html'
    session_id = request.COOKIES.get('session_id')
    

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid

    account_name = details.account_name
    branch = details.branch
    
    unlimited = details.unlimited  

    codes = Usercode.objects.filter(client_id=client_id)

    return render(request, template_name, {
        'codes': codes,
        'pid': client_id,
        'branch':branch,
        'account_name':account_name,
        'session_id':session_id, 
        'unlimited': unlimited,
    })





def load_code(request):
    template_name = 'superuser/codes.html'

    if request.method == 'GET': 
        member_id = request.GET.get('member_id')

    
        code = random.randint(10000, 99999)
        chars = random_char(3)
        usercode = f'{chars}{code}'
    
        try:
            existing_code = Usercode.objects.get(usercode=usercode).usercode

            while True:
                if usercode == existing_code:
                    code = random.randint(10000, 99999)
                    chars = random_char(3)
                    usercode = f'{chars}{code}'
                else:
                    break    

        except:
            pass

        membercode = Usercode.objects.get(member_id=member_id) 
        membercode.usercode = usercode    
        membercode.save()  


        try:
            all_assigned = AssignPaymentDuration.objects.filter(member_id=member_id)

            for assigned in all_assigned:
                assigned.usercode = usercode
                assigned.save() 

            token = ClientDetails.objects.get(pid=membercode.client_id).token

            url = f"https://db-api-v2.akwaabasoftware.com/members/user/{member_id}"

            payload = json.dumps({})
            headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json','Cookie': 'csrftoken=MmSz4Xh2CHMcrgt1chJAlu27V1FZvTjL2KUbJ9nqbaQw3fsCIUeebhhdigNSyZI4; sessionid=qvjnfg4gj0wey2swhm50ws0sy2hnx0az'}

            person = requests.request("GET", url, headers=headers, data=payload).json()['data']


            # firstname = person['firstname']
            # middlename = person['middlename']
            # surname = person['surname']
            # member_id = person['id']
            email = person['email']
            # phone = person['phone']
            # status = person['status']

            # if middlename == "":
            #     username = f"{firstname} {surname}"
            # else:
            #     username = f"{firstname} {middlename} {surname}"          


            # Send email
            # subject = f'RESET ACCESS CODE'
            # body = f"""
            #             Hello {username}, 
            #             Your new or updated invoice/bill from {company.company_name}. 
            #             Go to https://payfees.akwaabasoftware.com and enter {usercode} as your ACCESS CODE for details.
            #             Many thanks from {company.company_name}.
            #             Thank you.
            #         """
            # senders_mail = settings.EMAIL_HOST_USER
            # to_address = [f'{email}']

            # to_address = ['impraimgideon89@gmail.com']
            # email = EmailMessage(subject, body, senders_mail, to_address)
            # try:
            #     email.send()
            # except: 
            #     print("Server error")
            #     pass

            try:
                email_url = f'https://super.akwaabasoftware.com/api/client-email/{membercode.client_id}/'
                email = requests.request("GET", email_url, headers=headers, data=payload).json()['email']    
                password = requests.request("GET", email_url, headers=headers, data=payload).json()['password'] 

                EMAIL_BACKEND = env('EMAIL_BACKEND')
                EMAIL_HOST = env('EMAIL_HOST')
                EMAIL_USE_TLS = env('EMAIL_USE_TLS')
                EMAIL_PORT = env('EMAIL_PORT')
                EMAIL_HOST_USER = email
                EMAIL_HOST_PASSWORD = password

            except:

                EMAIL_BACKEND = env('EMAIL_BACKEND')
                EMAIL_HOST = env('EMAIL_HOST')
                EMAIL_USE_TLS = env('EMAIL_USE_TLS')
                EMAIL_PORT = env('EMAIL_PORT')
                EMAIL_HOST_USER = env('EMAIL_HOST_USER')
                EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
            

            try:
                company_name = InvoiceDetails.objects.filter(client_id=membercode.client_id).first().company_name
            except:
                company_name = "Client Service Alert"    

            # Send email
            subject = f'RESET ACCESS CODE'
            body = f"""
                    Hello {membercode.member}, 

                    Your new or updated invoice/bill from {company_name}. 
                    Go to https://unaapp.org and enter {usercode} as your ACCESS CODE for details.
                    Many thanks from {company_name}.
                    Thank you.
                    """
            senders_mail = EMAIL_HOST_USER
            to_address = [f'{email}']


            email = EmailMessage(subject, body, senders_mail, to_address)

            try:
                email.send()
            except: 
                print("Server error")
                pass


        except:
            pass    

        return render(request, template_name, {
            })



def load_invoice(request):
    template_name = 'superuser/test2.html'
    data = []
    amounts = []

    if request.method == 'GET': 
        branch = request.GET.get('branch')
        member_category = request.GET.get('member_category')
        group = request.GET.get('group')
        subgroup = request.GET.get('subgroup')
        fee_type = request.GET.get('fee_type')
        total_invoice = Invoice.objects.filter(fee_type=fee_type, branch=branch, member_category=member_category, group=group, subgroup=subgroup)
        
        for i in total_invoice.values():
             data.append(i)
        for x in range(len(data)):
             amounts.append(data[x]['total_amount']) 
        # print(amounts) 

        amount = [int(k) for k in amounts]

        return render(request, template_name, {
            'total_invoice': total_invoice,
            'amount': amount 
            })

    

def viewPaymentDuration(request, **kwargs):

    template_name = 'superuser/view-payment-details.html'
    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid


    account_name = details.account_name
    branch = details.branch
    
    unlimited = details.unlimited  



    try:
        base = Currency.objects.get(client_id=client_id, base=True).currency
    except:
        base = 'GHS'   


    assigned_payments = AssignPaymentDuration.objects.filter(client_id=client_id).order_by('-id')



    if request.method == 'GET':
        my_filter = AssignPaymentDurationFilter(request.GET, queryset=assigned_payments)
        assigned_payments = my_filter.qs



    return render(request, template_name, {
        'my_filter': my_filter,
        'assigned_payments': assigned_payments,
        'pid': client_id,
        'branch':branch,
        'account_name':account_name, 
        'base': base,
        'session_id':session_id,
        'unlimited': unlimited,
    }) 




# Delete payment duration
def deletePaymentDuration(request, id, **kwargs):

    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    branch = details.branch
    fullname = details.fullname   


    payment_duration = AssignPaymentDuration.objects.get(id=id)
    payment_duration.delete()

    activity = ActivityLog(user=fullname, branch=branch, client_id=client_id, action=f'deleted fee assigned to {payment_duration.member}')    
    activity.save()

    messages.success(request, 'Assigned invoice deleted successfully!')
    return redirect('superuser:viewPaymentDuration')







def makePayments(request, **kwargs):

        template_name = 'superuser/make-payment-2.html'
        pk = kwargs.get('pk')
        session_id = request.COOKIES.get('session_id')

        details = ClientDetails.objects.get(session_id=session_id)

        client_id = details.pid
        token = details.token
        email = details.email  
        account_name = details.account_name
        branch = details.branch
        fullname = details.fullname 

        firstname = details.firstname
        surname =  details.surname
        email = details.email
        phone = details.phone

        base = "GHS"


        # members = Members.objects.all()
        assigned = get_object_or_404(AssignPaymentDuration, pk=pk)
        # print(assigned)

        # print(assigned.deactivate == "True")
        organizations = InvoiceDetails.objects.filter(client_id=client_id).first()

        # print(assigned.deactivate == True)

        try:
            date = assigned.end_date.strftime('%Y-%m-%d')
        except:
            date = None    
        # date = assigned.end_date
        
        today = datetime.date.today()
        last_paid = datetime.datetime.today().strftime("%Y-%m-%d")
        year = datetime.datetime.now().year
        today = datetime.datetime.now()
        year = str(year) + "0000"


        payload = json.dumps({})
        headers = {}

        service_url = f"https://super.akwaabasoftware.com/api/service-fee/{client_id}/"

        try:
            service_charge = requests.request("GET", service_url, headers=headers, data=payload).json()['service_fee']
        except:
            service_charge = 0

    

        try:
            balance = Balance.objects.get(member_id=assigned.member_id).credit
        except:
            balance = 0



        try:
            email_url = f'https://super.akwaabasoftware.com/api/client-email/{client_id}/'
            client_email = requests.request("GET", email_url, headers=headers, data=payload).json()['email']    
            client_password = requests.request("GET", email_url, headers=headers, data=payload).json()['password'] 

            EMAIL_BACKEND = env('EMAIL_BACKEND')
            EMAIL_HOST = env('EMAIL_HOST')
            EMAIL_USE_TLS = env('EMAIL_USE_TLS')
            EMAIL_PORT = env('EMAIL_PORT')
            EMAIL_HOST_USER = client_email
            EMAIL_HOST_PASSWORD = client_password

        except:

            EMAIL_BACKEND = env('EMAIL_BACKEND')
            EMAIL_HOST = env('EMAIL_HOST')
            EMAIL_USE_TLS = env('EMAIL_USE_TLS')
            EMAIL_PORT = env('EMAIL_PORT')
            EMAIL_HOST_USER = env('EMAIL_HOST_USER')
            EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
        

        try:
            company_name = InvoiceDetails.objects.filter(client_id=client_id).first().company_name
        except:
            company_name = "Client Service Alert"  


        if request.method == 'POST':
            branch = request.POST.get('branch')
            member_category = request.POST.get('member_category')
            group = request.POST.get('group')
            subgroup = request.POST.get('subgroup')
            member = request.POST.get('member')
            member_id = request.POST.get('member_id')

            fee_type_id = request.POST.get('fee_type')
            fee_type = FeeType.objects.get(id=fee_type_id) 

            fee_description_id = request.POST.get('fee_description')
            fee_description = FeeDescription.objects.get(id=fee_description_id) 

            fee_type_value = fee_type.fee_type
            fee_description_value = fee_description.fee_description

            outstanding_bill = request.POST.get('outstanding_bill')
            payers_first_name = request.POST.get('payers_first_name')
            payers_last_name = request.POST.get('payers_last_name')
            contact = request.POST.get('contact')
            email_address = request.POST.get('email_address')
            remarks = request.POST.get('remarks')
            user_type = request.POST.get('user_type')
            invoice_type = request.POST.get('invoice_type')

            

            assigned_duration = request.POST.get('assigned_duration')
            # renewal_bill = request.POST.get('renewal_bill')
            expiration_bill = request.POST.get('expiration_bill')

            # print(expiration_bill)

            install_range = request.POST.get('install_range')
            install_period = request.POST.get('install_period')

            total_amount_due = request.POST.get('total_amount_due')
            outstanding_balance = request.POST.get('outstanding_balance')
            amount_paid = request.POST.get('amount_paid')
            payment_status = request.POST.get('payment_status')

            charge = request.POST.get('charge')
            
            end_date = request.POST.get('end_date')

            if payment_status == 'full':
                arrears = 0
            else:    
                arrears=request.POST.get('arrears')





            # print(assigned.deactivate)
            expiry = datetime.datetime.strptime(end_date, '%Y-%m-%d')

            if assigned.deactivate == True:
                if install_range == 'Day(s)':
                    subscription_expiry =  today + datetime.timedelta(days=(int(install_period)))
                elif install_range == 'Month(s)':  
                    subscription_expiry =  today + datetime.timedelta(days=(int(install_period) * 30))
                elif install_range == 'Year(s)':    
                    subscription_expiry =  today + datetime.timedelta(days=(int(install_period) * 365))
                else:
                    subscription_expiry = expiry 
            else:
                subscription_expiry = None 


            expiry = datetime.datetime.strptime(end_date, '%Y-%m-%d')
  
            if subscription_expiry > expiry:
                subscription_expiry = expiry 

            # print(subscription_expiry)  

              
            # print(subscription_expiry > end_date)


            if int(amount_paid) > int(total_amount_due):
                if int(arrears) <= 0:
                    credit= int(amount_paid) - int(total_amount_due)
            else:
                credit = 0     
                 


            url = f"https://db-api-v2.akwaabasoftware.com/members/user/{member_id}"

            payload = json.dumps({})
            headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json','Cookie': 'csrftoken=MmSz4Xh2CHMcrgt1chJAlu27V1FZvTjL2KUbJ9nqbaQw3fsCIUeebhhdigNSyZI4; sessionid=qvjnfg4gj0wey2swhm50ws0sy2hnx0az'}

            person = requests.request("GET", url, headers=headers, data=payload).json()['data']


            firstname = person['firstname']
            middlename = person['middlename']
            surname = person['surname']
            member_id = person['id']
            email = person['email']
            phone = person['phone']


            if middlename == "":
                username = f"{firstname} {surname}"
            else:
                username = f"{firstname} {middlename} {surname}" 


            make_payments = MakePayment(
                            branch=branch,
                            member_category=member_category,
                            group=group,
                            subgroup=subgroup,
                            member=username,
                            member_id=member_id,
                            client_id=client_id,
                            fee_type=fee_type,
                            fee_description=fee_description,
                            fee_type_value=fee_type_value,
                            fee_description_value=fee_description_value,
                            outstanding_bill=outstanding_bill,
                            payers_first_name=payers_first_name,
                            payers_last_name=payers_last_name,
                            contact=contact,
                            email_address=email_address,
                            remarks=remarks,
                            user_type=user_type,
                            assigned_duration=assigned_duration,
                            invoice_type=invoice_type,
                            install_range=install_range,
                            install_period=install_period,

                            # renewal_bill=renewal_bill,
                            expiration_bill=expiration_bill,

                            total_amount_due=total_amount_due,
                            outstanding_balance=outstanding_balance,
                            amount_paid=amount_paid,
                            payment_status=payment_status,
                            end_date=end_date,
                            subscription_expiry=subscription_expiry,
                            arrears=arrears,
                            credit=credit,
                            confirmed=True,
                            invoice_id=pk,
                            )
            make_payments.save()  

            invoice_no = f'FMS{int(year)+make_payments.id}'

            
            make_payments.invoice_no = invoice_no  
            make_payments.save() 


            payment = TotalPayments(member=member, member_id=member_id, client_id=client_id, payment=amount_paid, branch=branch, member_category=member_category, group=group, subgroup=subgroup)
            payment.save()


            # try:
            #     offline = OfflinePayments.objects.get(client_id=client_id, branch=branch, member_category=member_category, group=group, subgroup=subgroup)
            #     offline.total += float(amount_paid)
            #     offline.save()
            # except:

            offline = OfflinePayments.objects.create(client_id=client_id, total=amount_paid, branch=branch, member_category=member_category, group=group, subgroup=subgroup)
            offline.save()




            # try:
            #     service = ServiceFee.objects.get(client_id=client_id)
            #     service.amount += float(charge)
            #     service.save()

            # except:
            #     service = ServiceFee.objects.create(client_id=client_id, amount=charge)
            #     service.save()



            out_url = f"https://super.akwaabasoftware.com/api/outstanding-service-fee/"
            payload = json.dumps({"client_id":client_id, "service_fee": float(charge), "action":"increase"})
            headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}
            try:
                served = requests.request("POST", out_url, headers=headers, data=payload).json()['success']
            except:
                pass     




            # assigned.total_invoice = assigned.total_invoice - int(amount_paid)
            # print(expiration_bill is None)

            if expiration_bill is not None:
                if int(expiration_bill) > 0:
                    assigned.expiration_bill = int(expiration_bill) - int(amount_paid)
                    assigned.save()
                else:
                    assigned.expiration_bill = assigned.total_invoice  - int(amount_paid)
                    assigned.save()
            else:
                assigned.expiration_bill = assigned.total_invoice  - int(amount_paid)
                assigned.save()



            make_payments.amount_left = int(assigned.expiration_bill)  
            make_payments.save()   



            try:
                balance = Balance.objects.get(member=member, member_id=member_id)
                balance.credit = credit
                balance.save()
            except:
                balance = Balance(member=member, member_id=member_id, credit=credit)
                balance.save()







            # Send email
            subject = f'PAID {fee_type}'
            body = f"""
                        Hi {username}, 
                        An amount of GHc {amount_paid} has been paid as {payment_status} payment for {fee_description} by {payers_first_name} {payers_last_name}. 
                        The outstanding bill is {arrears}. 
                        Many thanks  from {company_name}.
                    """
            senders_mail = EMAIL_HOST_USER
            to_address = [f'{email}']

            email = EmailMessage(subject, body, senders_mail, to_address)

            try:
                email.send()
            except: 
                print("Server error")
                pass



            # # Send SMS
            private_key = env('PRIVATE_KEY')
            public_key = env('PUBLIC_KEY')

            if phone.startswith('0'):
                phone = f'233{int(phone)}'


            body = f"""
                        Hello {username}, 

                        An amount of GHc{amount_paid} has been paid as {payment_status} payment for 
                        {fee_description} by {payers_first_name} {payers_last_name}.
                        The outstanding bill is {arrears}. 
                        Many thanks  from {company_name}.

                    """

            url = f"https://api.msmpusher.net/v1/send?privatekey={private_key}&publickey={public_key}&sender=UNAGH&numbers={phone}&message={body}"

            payload = {}
            headers = {}

            try:
                response = requests.request("GET", url, headers=headers, data=payload).json()
            except:
                pass



            try:
                company = InvoiceDetails.objects.filter(client_id=client_id).first()
            except:
                pass  


            detail = get_object_or_404(MakePayment, pk=make_payments.id)

            try:
                invoice = Invoice.objects.get(fee_type= detail.fee_type, branch= detail.branch, member_category= detail.member_category, group= detail.group, subgroup= detail.subgroup)
            except:
                    try:
                        invoice = PrinterInvoice.objects.get(fee_type= detail.fee_type, branch= detail.branch, member_category= detail.member_category, group= detail.group, subgroup= detail.subgroup, total_amount=detail.outstanding_bill)
                    except:
                        return HttpResponse("If you are seeing this, then the invoice matching this query has either been modified or deleted")    

            keys = [item.fee_items for item in invoice.fee_items.all()]
            values = ["{:,}".format(int(i)) for i in invoice.items_amount.split(',')]
            data = dict(zip(keys, values))


            template = get_template('superuser/user_printer.txt')
            context = {
                'detail': detail,
                'company': company, 
                'invoice': invoice,
                'data': data
                }



            message = template.render(context)
            email = EmailMultiAlternatives(subject, message, senders_mail, [to_address])
            email.content_subtype = 'html'

            try:
                email.send()
            except: 
                print("Server error")
                pass



            activity = ActivityLog(user=fullname, branch=branch, action=f'paid an amount of GHc{amount_paid} for {member}')    
            activity.save()

            messages.success(request, 'Payment made successfully!')
            return redirect('superuser:viewPayments')

       
        else:
  
            return render(request, template_name, {
            'assigned': assigned, 
            'dated': date, 
            'firstname':firstname, 
            'surname':surname, 
            'email':email, 
            'phone':phone, 
            'period': AssignPeriod.objects.all(),
            'organizations':organizations,
            'service_charge':service_charge,
            'balance': balance,
            'pid':client_id,
            'branch':branch,
            'account_name':account_name,  
            'base':base,
            'session_id':session_id           
            })





def load_fee(request):
    template_name = 'superuser/member-fee-type.html'
    fee_types =[]

    if request.method == 'GET': 
        member = request.GET.get('member')

        user_type = AssignPaymentDuration.objects.filter(member=member)
        item = []
        items = []

        for i in user_type.values():   
            item.append(i)
        for x in range(len(item)):
            items.append(item[x]['fee_type_id'])    
        
        for k in items:
            fee_types.append(FeeType.objects.get(id=int(k))) 
        
        return render(request, template_name, {
            'fee_types' : fee_types,
            'user_type' : user_type,
            })



def load_balance(request):
    template_name = 'superuser/member-payment.html'
    fee_type = FeeType.objects.all()


    if request.method == 'GET': 
        fee_type = request.GET.get('fee_type')
        member = request.GET.get('member')
        balance = AssignPaymentDuration.objects.get(member=member, fee_type=fee_type)
        date = balance.end_date.strftime('%Y-%m-%d')
        # print(date)

        return render(request, template_name, {
            'balance' : balance,
            'date': date,
            })







def load_amount_due(request):
    template_name = 'superuser/amount_due.html'

    if request.method == 'GET': 
        assigned_id = request.GET.get('id')
        assigned_range = request.GET.get('range')
        assigned_period = request.GET.get('period')

        days = AssignPaymentDuration.objects.get(id=assigned_id)
        
        if assigned_range == 'Day(s)':
            total_amount_due =  int(assigned_period ) * int(days.amount_by_days)
        elif assigned_range == 'Month(s)':  
            total_amount_due =  int(assigned_period ) * 30 * int(days.amount_by_days)
        elif assigned_range == 'Year(s)':    
            total_amount_due =  int(assigned_period ) * 365 * int(days.amount_by_days)

        # print(total_amount_due)    
        # print(days.amount_by_days)  

        if total_amount_due >= days.expiration_bill:
            total_amount_due = days.expiration_bill

        # total_amount_due = 0   



        return render(request, template_name, {
            'total_amount_due': total_amount_due
            })



def load_credit(request):
    template_name = 'superuser/credit.html'

    if request.method == 'GET': 
        member = request.GET.get('member')
        member_id = request.GET.get('member_id')

        credit = Balance.objects.filter(member=member)

    return render(request, template_name, {
            'credit': credit
            })





def viewPayments(request, **kwargs):

    template_name = 'superuser/view-payments.html'
    today = datetime.date.today()

    
    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
 
    account_name = details.account_name
    branch = details.branch

    unlimited = details.unlimited  

    payments = MakePayment.objects.filter(client_id=client_id, confirmed=True)


    try:
        base = Currency.objects.get(client_id=client_id, base=True).currency
    except:
        base = 'GHS'    


    if request.method == 'GET':
        my_filter = PaymentsFilter(request.GET, queryset=payments)
        payments = my_filter.qs
    

    return render(request, template_name, {
        'my_filter': my_filter,
        'payments': payments,
        'today': today,
        'base': base,
        'pid': client_id,
        'branch':branch,
        'account_name':account_name, 
        'session_id':session_id,
        'unlimited': unlimited,        
    }) 





def viewDetails(request, **kwargs):
    # if ClientDetails.objects.count() > 0:

    template_name = 'superuser/view-detail.html'
    pk = kwargs.get('pk')
    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid

    account_name = details.account_name
    branch = details.branch



    try:
        base = Currency.objects.get(client_id=client_id, base=True).currency
    except:
        base = "GHS"


    payment = get_object_or_404(MakePayment, pk=pk)

    return render(request, template_name, {'session_id':session_id, 'payment': payment, 'base':base, 'pid': client_id, 'branch':branch, 'account_name':account_name, })

  



def viewAssigned(request, **kwargs):

    template_name = 'superuser/view-assigned.html'
    pk = kwargs.get('pk')
    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
 
    account_name = details.account_name
    branch = details.branch
 
    base = Currency.objects.get(client_id=client_id, base=True)
    assigned = get_object_or_404(AssignPaymentDuration, pk=pk)

    return render(request, template_name, {'session_id':session_id, 'assigned': assigned, 'base':base, 'pid': client_id, 'branch':branch, 'account_name':account_name, })




def viewInvoices(request, **kwargs):
    
    template_name = 'superuser/view-invoices.html'

    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid

    account_name = details.account_name
    branch = details.branch

    unlimited = details.unlimited  


    base = Currency.objects.get(client_id=client_id, base=True)
    pk = kwargs.get('pk')
    invoice = get_object_or_404(Invoice, pk=pk)

    return render(request, template_name, {'unlimited': unlimited, 'session_id':session_id, 'invoice': invoice, 'base':base, 'pid': client_id, 'branch':branch, 'account_name':account_name, })







def viewOrganizationDetail(request, **kwargs):


    template_name = 'superuser/view-organization.html'
    pk = kwargs.get('pk')

    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
 
    account_name = details.account_name
    branch = details.branch
 
    unlimited = details.unlimited  

    organizations = get_object_or_404(InvoiceDetails, pk=pk)

    return render(request, template_name, {'unlimited': unlimited, 'organizations': organizations, 'pid':client_id, 'branch':branch, 'account_name':account_name, 'session_id':session_id})






def delete_payment(request, *args, **kwargs):

    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid

    branch = details.branch
    fullname = details.fullname    


    if request.method == "POST":

        payment_ids = request.POST.getlist('id[]')

        for payment_id in payment_ids:
            payment = MakePayment.objects.get(pk=payment_id)
            payment.delete()

        activity = ActivityLog(user=fullname, branch=branch, client_id=client_id, action=f'deleted payment')    
        activity.save()    

    messages.success(request, 'Payment record deleted successfully!')
    return redirect('superuser:viewPayments') 


        # return redirect('superuser:viewPayments' client_id) 

        # return HttpResponseRedirect('/view-payments')   



def delete_assigned(request, *args, **kwargs):

    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
 


    if request.method == "POST":
        assigned_ids = request.POST.getlist('id[]')

        for assigned_id in assigned_ids:
            assigned = AssignPaymentDuration.objects.get(pk=assigned_id)
            assigned.delete()

        messages.success(request, 'Assigned invoice(s) deleted successfully!')
        return redirect('superuser:viewPaymentDuration') 




def delete_invoice(request, *args, **kwargs):

    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid


    if request.method == "POST":
        invoice_ids = request.POST.getlist('id[]')

        for invoice_id in invoice_ids:
            invoice = Invoice.objects.get(pk=invoice_id)
            invoice.delete()

        messages.success(request, 'Invoice(s) deleted successfully!')
        return redirect('superuser:viewInvoice') 



def viewProfile(request, **kwargs):

    template_name = 'superuser/profile.html'
    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    account_name = details.account_name
    branch = details.branch

    url = f"https://db-api-v2.akwaabasoftware.com/clients/account/{client_id}"
    
    headers = {
                'Authorization': f'Token {token}',
                'Content-Type': 'application/json',
                'Cookie': 'csrftoken=4qQVgGyOrmGlgdMwQwsuRh9jmnTOyPSbjOI6Vm4VQLxX9O7gKkWr3DufNXYd7RVH; sessionid=0e2td1b1uzn4cjb5naw9bjw1hs9sjzxw'
                }

    response = requests.request("GET", url, headers=headers).json()['data']
    # print(response)

    return render(request, template_name, {'response': response, 'pid':client_id,
                'branch':branch,
            'account_name':account_name, 'session_id':session_id})






def viewClientProfile(request, **kwargs):

    template_name =  'superuser/client-profile.html' 
    member_id = kwargs.get('id')
    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token  
    account_name = details.account_name
    branch = details.branch

    url = f"https://db-api-v2.akwaabasoftware.com/members/user/{member_id}"

    payload = json.dumps({})
    headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json','Cookie': 'csrftoken=MmSz4Xh2CHMcrgt1chJAlu27V1FZvTjL2KUbJ9nqbaQw3fsCIUeebhhdigNSyZI4; sessionid=qvjnfg4gj0wey2swhm50ws0sy2hnx0az'}

    member = requests.request("GET", url, headers=headers, data=payload).json()['data']

    return render(request, template_name, {'member': member, 'pid': client_id,
                'branch':branch,
            'account_name':account_name, 'session_id':session_id}) 






def viewMembers(request, **kwargs):

    template_name = 'superuser/members.html'
    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token 
    account_name = details.account_name
    branch = details.branch

    members_url = f"https://db-api-v2.akwaabasoftware.com/members/user?datatable_plugin&length=1000"

    payload = json.dumps({})


    members_headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=Ly8oYWb8c70C2CDUYfFd0poVjCL91Octs99w3q6rGjSu8L2SaPVDoGPvJ4tKQIda; sessionid=4zyr1pvz9r6hyu8sqvuh0gqqxsymo56n'
    }


    members = requests.request("GET", members_url, headers=members_headers, data=payload).json()['data']


    return render(request, template_name, {                    
    'all_members': members,
    'pid': client_id,
    'branch':branch,
    'account_name':account_name, 
    'session_id':session_id
    })        
                        





def viewActivityLog(request, **kwargs):

    template_name = 'superuser/activity-log.html'


    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    account_name = details.account_name
    branch = details.branch
    
    unlimited = details.unlimited  

    activities = ActivityLog.objects.filter(client_id=client_id).order_by('-id')


    if request.method == 'GET':
        my_filter = ActivitiesFilter(request.GET, queryset=activities)
        all_activities = my_filter.qs
 

    return render(request, template_name, {
        'activities': all_activities,
        'pid':client_id,
        'branch':branch,
        'account_name':account_name,
        'my_filter':my_filter, 
        'session_id':session_id,
        'unlimited': unlimited,
    })








# def createDonation(request):
#     if ClientDetails.objects.count() > 0:

#         admin = user['firstname'] +' '+ user['surname']
#         template_name = 'superuser/create-donation.html'

#         if request.method == 'POST':
#             donation_name = request.POST.get('donation_name')
#             amount = request.POST.get('target_amount')

#             if amount == "":
#                 target_amount = 0
#             else:
#                 target_amount=amount    

#             donation = Donation(donation_name=donation_name, target_amount=target_amount)
#             donation.save()

#             activity = ActivityLog(user=admin, action=f'created {donation_name}')    
#             activity.save()

#             messages.success(request, 'Donation created successfully!')
#             return HttpResponseRedirect(reverse('superuser:viewDonations')) 
#         else:
#             return render(request, template_name, {

#             })
            
#     else:
#         messages.error(request, 'Please Login to continue') 
#         return HttpResponseRedirect(reverse('login:login'))         

    


# def viewDonations(request):
#     if ClientDetails.objects.count() > 0:

#         template_name = 'superuser/donations.html'
#         donations = Donation.objects.all()


#         return render(request, template_name, {
#             'donations': donations
#         })
#     else:
#         messages.error(request, 'Please Login to continue') 
#         return HttpResponseRedirect(reverse('login:login'))         



# def viewDonation(request, **kwargs):
#     if ClientDetails.objects.count() > 0:

#         template_name = 'superuser/view-donation.html'
#         # donations = Donation.objects.all()
#         pk = kwargs.get('id')
#         donation = get_object_or_404(Donation, pk=pk)
#         organizations = get_object_or_404(InvoiceDetails, pk=1)


#         return render(request, template_name, {
#             'donation': donation,
#             'organizations': organizations,
#         })
#     else:
#         messages.error(request, 'Please Login to continue') 
#         return HttpResponseRedirect(reverse('login:login'))         




# def assignDonation(request, **kwargs):
#     if ClientDetails.objects.count() > 0:

#         admin = user['firstname'] +' '+ user['surname']

#         template_name = 'superuser/assign-donation.html'
#         pk = kwargs.get('pk')
#         donation = get_object_or_404(Donation, pk=pk)
#         today = datetime.datetime.now()
#         company = InvoiceDetails.objects.all().first()
#         some_members = Members.objects.all()[:15]
#         total_members = Members.objects.all()


#         if request.method == 'POST':
#             donation_name = request.POST.get('donation_name')
#             target_amount = request.POST.get('target_amount')
#             member = request.POST.get('member')
#             all_members = request.POST.get('all_members')

#             if target_amount == "None":
#                 total_invoice = 0
#             else:
#                 total_invoice=target_amount 


#             if all_members == "all_members":
#                 # print("all")
#                 for member in total_members:
#                     print(member.member)
#                     assignPayments = AssignPaymentDuration(donation_name = donation_name, member = member.member, total_invoice = total_invoice)
#                     assignPayments.save()


#                     # Send email
#                     subject = f'ASSIGNED {donation_name}'
#                     body = f"""
#                                 Hello {member.member}, 
#                                 A donation of {donation_name} has been assigned to you at any amount. 
#                                 Many thanks  from {company.company_name}
#                             """
#                     senders_mail = settings.EMAIL_HOST_USER
#                     to_address = [f'{member.email_address}']

#                     # send_mail(subject, body, senders_mail, to_address, fail_silently=False)
#                     # html_template = 'superuser/user_printer.html'

#                     # html_message = render_to_string(html_template)
#                     email = EmailMessage(subject, body, senders_mail, to_address)
#                     try:
#                         email.send()
#                     except: 
#                         print("Server error")
#                         pass

#                     # Send SMS
#                     message = f"""
#                                 Hello {member.member}, 
#                                 A donation of {donation_name} has been assigned to you at any amount. 
#                                 Many thanks  from {company.company_name}
#                             """

#                     payload= json.dumps({
#                                 "token": f'{msg}',
#                                 "message_numbers": [f'{member.contact}'],
#                                 "message_body": message,
#                                 "sender_id": "nstacom",
#                                 "subject": "Assigned {fee_type}",
#                                 "schedule": f'{today.strftime("%Y-%m-%d %H:%M:%S")}'
#                                 # "schedule": "2022-06-12 05:30:53"
#                         })
#                     files=[]
#                     headers = { 
#                             'Content-Type': 'application/json',
#                             'Cookie': 'ci_session=207c8f86bebfac4e513b0558b353015141475c36'
#                             }

#                     response = requests.request("POST", sms_url, headers=headers, data=payload, files=files)
#                     print(response.text)

#                     message = Message(sms='sms', message=message, contact=f'{member.contact}')
#                     message.save()  
                    
#                 activity = ActivityLog(user=admin, action=f'assigned donation to all members')    
#                 activity.save() 

#             else:    
#                 assignPayments = AssignPaymentDuration(
#                                 donation_name = donation_name,
#                                 member = member,
#                                 total_invoice = total_invoice,                               
#                                )

#                 assignPayments.save()

#                 try:
#                     assigned_member = Members.objects.get(member=member)
#                 except:
#                     assigned_member = Members.objects.filter(member=member).first()  

#                 # Send email
#                 subject = f'ASSIGNED {donation_name}'
#                 body = f"""
#                             Hello {member}, 
#                             A donation of {donation_name} has been assigned to you at any amount. 
#                             Many thanks  from {company.company_name}
#                         """
#                 senders_mail = settings.EMAIL_HOST_USER
#                 to_address = [f'{assigned_member.email_address}']

#                 # send_mail(subject, body, senders_mail, to_address, fail_silently=False)
#                 # html_template = 'superuser/user_printer.html'

#                 # html_message = render_to_string(html_template)
#                 email = EmailMessage(subject, body, senders_mail, to_address)
#                 try:
#                     email.send()
#                 except: 
#                     print("Server error")
#                     pass

#                 # Send SMS
#                 message = f"""
#                             Hello {member}, 
#                             A donation of {donation_name} has been assigned to you at any amount. 
#                             Many thanks  from {company.company_name}
#                         """

#                 payload= json.dumps({
#                             "token": f'{msg}',
#                             "message_numbers": [f'{assigned_member.contact}'],
#                             "message_body": message,
#                             "sender_id": "nstacom",
#                             "subject": "Assigned {fee_type}",
#                             "schedule": f'{today.strftime("%Y-%m-%d %H:%M:%S")}'
#                             # "schedule": "2022-06-12 05:30:53"
#                     })
#                 files=[]
#                 headers = { 
#                         'Content-Type': 'application/json',
#                         'Cookie': 'ci_session=207c8f86bebfac4e513b0558b353015141475c36'
#                         }

#                 response = requests.request("POST", sms_url, headers=headers, data=payload, files=files)
#                 print(response.text)

#                 message = Message(sms='sms', message=message, contact=f'{assigned_member.contact}')
#                 message.save()  
                
#                 activity = ActivityLog(user=admin, action=f'assigned donation to {member}')    
#                 activity.save() 


#             if len(PrinterDonation.objects.filter(donation_name=donation.donation_name, target_amount=donation.target_amount)) > 0:
#                 pass
#             else:
#                 printer_donation = PrinterDonation(donation_name=donation.donation_name, target_amount=donation.target_amount)
#                 printer_donation.save()

#             messages.success(request, 'Donation(s) assigned successfully!')

#             return HttpResponseRedirect(reverse('superuser:viewPaymentDuration')) 
#             # return HttpResponseRedirect('/view-payment-details')
#         else:
#             return render(request, template_name, {
#                 'donation': donation,
#                 'some_members': some_members,
#             })   

#     else:
#         messages.error(request, 'Please Login to continue') 
#         return HttpResponseRedirect(reverse('login:login'))




# def payDonation(request, **kwargs):
#     if ClientDetails.objects.count() > 0:

#         admin = user['firstname'] +' '+ user['surname']
#         firstname = user['firstname']
#         surname =  user['surname']
#         email = user['email']
#         phone = user['phone']
        

#         template_name = 'superuser/pay-donation.html'

#         pk = kwargs.get('id')
#         members = Members.objects.all()
#         assigned = get_object_or_404(AssignPaymentDuration, pk=pk)
#         company = InvoiceDetails.objects.all().first()
#         organizations = get_object_or_404(InvoiceDetails, pk=1)
#         # print(organizations.logo)

        
#         today = datetime.date.today()
#         last_paid = datetime.datetime.today().strftime("%Y-%m-%d")
#         year = datetime.datetime.now().year
#         today = datetime.datetime.now()
#         year = str(year) + "0000"



#         if request.method == 'POST':
            
#             member = request.POST.get('member')
#             donation_name = request.POST.get('donation_name')

#             payers_first_name = request.POST.get('payers_first_name')
#             payers_last_name = request.POST.get('payers_last_name')
#             contact = request.POST.get('contact')
#             email_address = request.POST.get('email_address')

#             amount_paid = request.POST.get('amount_paid')
    
#             make_payments = MakePayment(
#                             member=member,
#                             donation_name=donation_name,
#                             payers_first_name=payers_first_name,
#                             payers_last_name=payers_last_name,
#                             contact=contact,
#                             email_address=email_address,
#                             amount_paid=amount_paid, 
#                             )
#             make_payments.save()  

#             # invoice_no = f'FMS{year}{month}{day}{make_payments.id}'
#             invoice_no = f'FMS{int(year)+make_payments.id}'

            
#             make_payments.invoice_no = invoice_no  
#             make_payments.save() 


#             if len(Members.objects.filter(member=member)) > 0:
#                 member = Members.objects.get(member=member)
#                 member.recently_paid = last_paid
#                 member.save()
#             else:
#                 pass  


#             if len(Donation.objects.filter(donation_name=donation_name)) > 0:
#                 donation = Donation.objects.get(donation_name=donation_name)
#                 donation.amount_received = int(donation.amount_received) + int(amount_paid)
#                 donation.save()
#             else:
#                 pass


#             try:
#                 paid_member = Members.objects.get(member=member)
#             except:
#                 paid_member = Members.objects.filter(member=member).first()  

#             # Send email
#             subject = f'Paid {donation_name}'
#             body = f"""
#                         Hi {member}, 
#                         An amount of GHc {amount_paid} has been paid as {donation_name} by {payers_first_name} {payers_last_name}. 
#                         Many thanks  from {company.company_name}.
#                     """
#             senders_mail = settings.EMAIL_HOST_USER
#             to_address = [f'{paid_member.email_address}']

#             send_mail(subject, body, senders_mail, to_address, fail_silently=False)




#             company = InvoiceDetails.objects.all().first()
#             detail = get_object_or_404(MakePayment, pk=make_payments.id)


#             template = get_template('superuser/donation_printer.txt')
#             context = {
#                 'detail': detail,
#                 'company': company, 
#                 }


#             message = template.render(context)
#             email = EmailMultiAlternatives(subject, message, senders_mail, to_address)
#             email.content_subtype = 'html'

#             try:
#                 email.send()
#             except: 
#                 print("Server error")
#                 pass




#             # Send SMS
#             message = f"""
#                         Hi {member}, 
#                         An amount of GHc {amount_paid} has been paid as {donation_name} by {payers_first_name} {payers_last_name} . 
#                         Many thanks  from {company.company_name}.
#                     """

#             payload= json.dumps({
#                         "token": f'{msg}',
#                         "message_numbers": [f'{paid_member.contact}'],
#                         "message_body": message,
#                         "sender_id": "nstacom",
#                         "subject": f"Paid {donation_name}",
#                         "schedule": f'{today.strftime("%Y-%m-%d %H:%M:%S")}'
#                         # "schedule": "2022-06-12 05:30:53"
#                 })
#             files=[]
#             headers = { 
#                     'Content-Type': 'application/json',
#                     'Cookie': 'ci_session=207c8f86bebfac4e513b0558b353015141475c36'
#                     }

#             response = requests.request("POST", sms_url, headers=headers, data=payload, files=files)
#             print(response.text)

#             message = Message(sms='sms', message=message, contact=f'{paid_member.contact}')
#             message.save()

#             activity = ActivityLog(user=admin, action=f'paid an amount of GHc{amount_paid} for {member} as {donation_name}')    
#             activity.save()

#             messages.success(request, 'Payment made successfully!')

#             return HttpResponseRedirect(reverse('superuser:viewPayments')) 
#             # return HttpResponseRedirect('/view-payments')        
#         else:
  
#             return render(request, template_name, {'assigned': assigned, 'organizations':organizations, 'firstname':firstname, 'surname':surname, 'email':email, 'phone':phone,})

#     else:
#         messages.error(request, 'Please Login to continue') 
#         return HttpResponseRedirect(reverse('login:login'))



# def viewPublicDonations(request):
#     if ClientDetails.objects.count() > 0:

#         template_name = 'superuser/view-public-donations.html'
#         public_donations = PublicDonation.objects.all()

#         return render(request, template_name, {
#             'public_donations': public_donations,
#         })

#     else:
#         messages.error(request, 'Please Login to continue') 
#         return HttpResponseRedirect(reverse('login:login'))



# def createPublicDonation(request):
#     if ClientDetails.objects.count() > 0:
#         template_name = 'superuser/create-public-donation.html'
#         company = InvoiceDetails.objects.all().first()
#         admin = user['firstname'] +' '+ user['surname']

#         if request.method == 'POST':
#             organization_name = request.POST.get('organization_name')
#             contact = request.POST.get('contact')
#             email = request.POST.get('email')
#             donation_name = request.POST.get('donation_name')
#             amount = request.POST.get('target_amount')
#             purpose = request.POST.get('purpose')
#             website = request.POST.get('website')


#             # code=''.join(random.choice(string.ascii_letters + string.digits) for x in range(8))

#             # payment_url=f"hhtps://akfms.com/payment={code}"

#             if amount == "":
#                 target_amount = 0
#             else:
#                 target_amount=amount  

#             public_donation = PublicDonation(
#                 organization_name=organization_name, 
#                 contact=contact, 
#                 email=email, 
#                 donation_name=donation_name, 
#                 target_amount=target_amount, 
#                 purpose=purpose,
#                 website=website,
#                 )
#             public_donation.save()

#             public_donation.payment_url =  f'/pay-public-donation/{public_donation.id}'
#             # public_donation.payment_url =  f"redirect('superuser:payPublicDonation' public_donation.id)"
#             public_donation.save()   

#             print(public_donation.payment_url)  

#             activity = ActivityLog(user=admin, action=f'created {donation_name}')    
#             activity.save()

#             messages.success(request, 'Public donation created successfully!')

#             return HttpResponseRedirect(reverse('superuser:viewPublicDonations')) 
#             # return HttpResponseRedirect('/view-payments')        
#         else:
#              return render(request, template_name, {
#             'company': company
#         })

#     else:
#         messages.error(request, 'Please Login to continue') 
#         return HttpResponseRedirect(reverse('login:login')) 



# def viewPublicDonation(request, **kwargs):
#     if ClientDetails.objects.count() > 0:
#         template_name = 'superuser/view-public-donation.html'

#         pk = kwargs.get('id')
#         public_donations = PublicDonation.objects.all()
#         public_donation = get_object_or_404(PublicDonation, pk=pk)
#         company = InvoiceDetails.objects.all().first()
#         organizations = InvoiceDetails.objects.all().first()

#         base_url = "https://fees.akwaabasoftware.com/"
#         link = base_url + f'client/pay-public-donation/{public_donation.id}'

#         shortener = pyshorteners.Shortener()
#         payment_link = shortener.tinyurl.short(link)


#         return render(request, template_name, {'public_donation': public_donation, 'organizations':organizations, 'payment_link': payment_link })

#     else:
#         messages.error(request, 'Please Login to continue') 
#         return HttpResponseRedirect(reverse('login:login')) 



# def editPublicDonation(request, id):
#     if ClientDetails.objects.count() > 0:
#         template_name = 'superuser/edit-public-donations.html'
#         company = InvoiceDetails.objects.all().first()

#         admin = user['firstname'] +' '+ user['surname']
#         organizations = get_object_or_404(InvoiceDetails, pk=1)

#         public_donation = PublicDonation.objects.get(id=id)
        
#         if request.method == 'POST':
#             public_donation.organization_name = request.POST.get('organization_name')
#             public_donation.donation_name = request.POST.get('donation_name')
#             public_donation.contact = request.POST.get('contact')
#             public_donation.email = request.POST.get('email')
#             public_donation.target_amount = request.POST.get('target_amount')
#             public_donation.purpose = request.POST.get('purpose')
#             public_donation.save()

#             activity = ActivityLog(user=admin, action=f'edited {public_donation}')    
#             activity.save()

#             messages.success(request, 'Public Donation edited successfully!')

#             return HttpResponseRedirect(reverse('superuser:viewPublicDonations')) 

#         else:    
#              return render(request, template_name, {'company': company, 'public_donation': public_donation, 'organizations':organizations})

#     else:
#         messages.error(request, 'Please Login to continue') 
#         return HttpResponseRedirect(reverse('login:login')) 



# def payPublicDonation(request, **kwargs):
#         template_name = 'superuser/pay-public-donation.html'

       
#         pk = kwargs.get('id')
#         public_donations = PublicDonation.objects.all()
#         public_donation = get_object_or_404(PublicDonation, pk=pk)
#         company = InvoiceDetails.objects.all().first()
#         organizations = get_object_or_404(InvoiceDetails, pk=1)

#         try:
#             all_currencies = Currency.objects.filter(base=True)

#             if len(all_currencies) > 0:
#                 base_currency = all_currencies.first().currency
#             else:
#                 base_currency = "GHS"    
#         except:
#                base_currency = "GHS"          


#         if request.method == "POST":
#             donation_name = request.POST.get('donation_name')
#             amount_paid = request.POST.get('amount_paid')
#             donor_name = request.POST.get('donors_name')
#             donor_contact = request.POST.get('contact')
#             donor_email = request.POST.get('email')
#             donor_country = request.POST.get('country')
#             currency = request.POST.get('currency')
#             remarks = request.POST.get('remarks')

#             if donor_name == "":
#                 donors_name = "Anonymous"
#             else: 
#                 donors_name = donor_name

#             if donor_contact == "":
#                 contact = "None"
#             else:
#                 contact = donor_contact


#             if donor_email == "":
#                 email = "None"
#             else:
#                 email = donor_email

#             if donor_country == "":
#                 country = "None" 
#             else:
#                 country = donor_country         

#             api_key='a61577a4f2a144c0fb6b6379'
#             url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{currency}/{base_currency}/{amount_paid}" 

#             payload={}
#             headers = {}

#             response = requests.request("GET", url, headers=headers, data=payload).json()
#             paid_amount = response['conversion_result']    


#             paid_public = PublicPayments(
#                 donation_name=donation_name, 
#                 amount_paid=paid_amount, 
#                 donors_name=donors_name,
#                 contact=contact,
#                 email=email,
#                 country=country,
#                 currency=currency,
#                 remarks=remarks,
#                 )

#             paid_public.save()   


#             public_donation.amount_paid = int(public_donation.amount_paid) + int(amount_paid) 
#             public_donation.save()

#             messages.success(request, 'Payment made successfully!')
#             return HttpResponseRedirect(reverse('superuser:thank_you')) 

#         else:
#              return render(request, template_name, {
#                 'public_donation': public_donation,
#                 'company': company,
#                 'organizations':organizations
#                 })



# def publicDonors(request):
#     if ClientDetails.objects.count() > 0:

#         template_name = 'superuser/public-donors.html'
#         public_donors = PublicPayments.objects.all().order_by('-id')

#         return render(request, template_name, {
#             'public_donors': public_donors,
#         })

#     else:
#         messages.error(request, 'Please Login to continue') 
#         return HttpResponseRedirect(reverse('login:login')) 



# def thank_you(request, **kwargs):
#     template_name = 'superuser/thank-you.html'
#     organizations = get_object_or_404(InvoiceDetails, pk=1)

#     return render(request, template_name, {
#         'organizations': organizations
#     })




# def deactivated(request):
#     template_name = 'superuser/deactivated.html'

#     return render(request, template_name, {})







def load_bill(request):
    template_name = 'superuser/bill.html'
    today = datetime.date.today()
    now = datetime.datetime.now()
    year = datetime.datetime.now().year
    year = str(year) + "0000"


    if request.method == "POST":
        amount_paid = request.POST.get('amount_paid')
        base = request.POST.get('base')
        client_id = request.POST.get('client_id')
        # subgroup = request.POST.get('subgroup')

        code = random.randint(10000, 99999)
        chars = random_char(3)
        invoice_no = f'{chars}{code}'

        #     out_url = "https://super.akwaabasoftware.com/api/outstanding-service-fee/"
        #     payload = json.dumps({"client_id":client_id, "service_fee": 0.00, "action":"decrease"})
        #     headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}

        #     try:
        #         served = requests.request("POST", out_url, headers=headers, data=payload).json()['success']
        #     except:
        #         pass 
       

        url = "https://payproxyapi.hubtel.com/items/initiate"
        
  
        returnUrl = f"https://cash.akwaabasoftware.com/superuser/"
        # returnUrl = f"http://127.0.0.1:5000/superuser/{client_id}/"


        payload = json.dumps({
                "totalAmount": amount_paid,
                "description": "Outstanding Service Payment",
                "callbackUrl": "https://transactions.akwaabasoftware.com/add-transaction/",
                "returnUrl": returnUrl,
                "merchantAccountNumber": "2017254",
                "cancellationUrl": "https://hubtel.com/",
                "clientReference": invoice_no
            })


        headers = {
        'Authorization': 'Basic UDc5RVdSVzozNmZmNzk3YTgyMjU0NzJmOTA2ZGU0NGM3NGVkZWE0Zg==',
        'Content-Type': 'application/json'
        }


        response = requests.request("POST", url, headers=headers, data=payload).json()['data']['checkoutUrl']

        
        return render(request, template_name, {'response': response})





def payService(request, *args, **kwargs):
    
    template_name = "superuser/pay-service.html"

    session_id = request.COOKIES.get('session_id')

    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid  
    account_name = details.account_name

    organizations = InvoiceDetails.objects.filter(client_id=client_id).first()

    payload = json.dumps({})
    headers = {}

    service_url = f"https://super.akwaabasoftware.com/api/service-fee/{client_id}/"

    try:
        limit = requests.request("GET", service_url, headers=headers, data=payload).json()['limit']

        outstanding = requests.request("GET", service_url, headers=headers, data=payload).json()['outstanding_fee']
        outstanding = float(outstanding)
    except:
        limit = 0.00
        outstanding = 0.00




    return render(request, template_name, { 
        'pid':client_id,
        'outstanding':outstanding,
        'account_name':account_name,
        'organizations':organizations,
        'limit': limit,
        'session_id':session_id
        })





def logout(request, id):
    
    response = HttpResponse("You have been logged out.")
    response.delete_cookie('session_id')

    subject = ClientDetails.objects.get(session_id=id)
    subject.delete()
    
    return redirect('login:login')