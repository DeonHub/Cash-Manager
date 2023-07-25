from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from superuser.models import AssignPaymentDuration, Currency, FeeType, FeeDescription, Invoice, PrinterInvoice, Balance, InvoiceDetails, TotalAmount, TotalPayments, MakePayment, Donation, AssignPeriod, PrinterDonation
from .models import *
import json
from django.urls import reverse
import datetime
# from fee_sys.auth import *
# from fee_sys.requests import *
# from fee_sys.login import msg
from django.contrib import messages
import requests
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives

# PDF stuff
from django.template.loader import get_template
from xhtml2pdf import pisa
import io
from django.http import FileResponse
from login.models import MemberDetails, ClientDetails
from api.models import Dasha




def invoice_details_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    client_id = kwargs.get('clid')
    
    try:
        base = Currency.objects.get(client_id=client_id, base=True)
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



def donation_details_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    client_id = kwargs.get('clid')
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





def index(request, **kwargs):

    template_name = 'client/index.html'
    member_id = kwargs.get('mid')


    try:
        details = MemberDetails.objects.filter(mid=member_id).last()
        member_account_name = details.account_name
        member_branch = details.branch
        mid = details.mid
        token = details.token
        client_id = details.client_id

        try:
            base = Currency.objects.get(client_id=client_id, base=True).currency
            
        except:
            base = 'GHS'    

        try:
            dasho = Dasha.objects.get(mid=mid)

            if dasho.redirected == True:
                setItem = True
            else:
                setItem = False
        except:
            setItem = False  


    except:
           token = ""
           member_account_name = "Demo Account"
           member_branch = "Other Branch"
           mid = 1
           setItem = False
           base = 'GHS'
           client_id = 1





    # token = os.environ.get('TOKEN')
    # print(token)
    total_invoice = 0
    total_payments = 0
    total_arrears = 0
    today = datetime.date.today()
    # this = today.year


    year_range = request.GET.get('year_range', today.year)

    if year_range:
        year = int(year_range)
    else:
        year = today.year


    temp_invoice = [int(invoice.total) for invoice in TotalAmount.objects.filter(member_id=member_id, date_created__year=year)]
    temp_payments = [int(invoice.payment) for invoice in TotalPayments.objects.filter(member_id=member_id, date_paid__year=year)]

    for i in temp_invoice:
        total_invoice += i

    for i in temp_payments:
        total_payments += i

    total_arrears = total_invoice - total_payments 

    try:
        collected= (total_payments / total_invoice)*100
    except ZeroDivisionError:
        collected=0

    amount_received= '{0:.2f}'.format(collected)

    total_arrears = total_invoice - total_payments
    string_payments = "{:,}".format(total_payments)
    string_invoice = "{:,}".format(total_invoice)
    string_arrears = "{:,}".format(total_arrears)

    return render(request, template_name, {
        'amount_received':amount_received,
        'string_payments':string_payments,
        'string_arrears':string_arrears,
        'string_invoice':string_invoice,
        'total_invoice': total_invoice,
        'total_payments': total_payments,
        'total_arrears': total_arrears,
        'token': token,
        'year': year,
        'member_account_name': member_account_name, 
        'member_branch':member_branch, 
        'mid':mid, 
        'token':token, 
        'setItem': setItem, 
        'base': base, 
        'clid':client_id
    })
 





def viewAssignedPayments(request, **kwargs):

    template_name = 'client/view-assigned-payments.html'
    member_id = kwargs.get('mid')


    try:
        details = MemberDetails.objects.filter(mid=member_id).last()
        member_account_name = details.account_name
        member_branch = details.branch
        mid = details.mid
        token = details.token
        client_id = details.client_id

        try:
            base = Currency.objects.get(client_id=client_id, base=True).currency
            
        except:
            base = 'GHS'    

        try:
            dasho = Dasha.objects.get(mid=mid)

            if dasho.redirected == True:
                setItem = True
            else:
                setItem = False
        except:
            setItem = False  


    except:
           token = ""
           member_account_name = "Demo Account"
           member_branch = "Other Branch"
           mid = 1
           setItem = False
           base = 'GHS'
           client_id = 1


    assigned = AssignPaymentDuration.objects.filter(member_id=member_id).order_by('-id')
    user = AssignPaymentDuration.objects.filter(member_id=member_id).first()
    # total = [int(invoice.total_invoice) for invoice in assigned]
    # print(assigned)
    
    return render(request, template_name,{
        'assigned': assigned,
        'user': user,
        'token': token,
        'member_account_name': member_account_name, 
        'member_branch':member_branch, 
        'mid':mid, 
        'token':token, 
        'setItem': setItem, 
        'base': base, 
        'clid':client_id
    })








def load_bill(request):
    template_name = 'client/bill.html'
    today = datetime.date.today()
    now = datetime.datetime.now()
    year = datetime.datetime.now().year
    # today = datetime.datetime.now()
    year = str(year) + "0000"



    # firstname = client.firstname
    # surname =  client.surname
    # email = client.email
    # phone = client.phone

    # # members = Members.objects.all()
    # # print(assigned)

    # # print(assigned.deactivate == "True")
    # organizations = InvoiceDetails.objects.filter(client_id=client_id).first()

    # # print(assigned.deactivate == True)

    # date = assigned.end_date.strftime('%Y-%m-%d')
    # balance = Balance.objects.all()
    # today = datetime.date.today()
    # last_paid = datetime.datetime.today().strftime("%Y-%m-%d")
    # year = datetime.datetime.now().year
    # today = datetime.datetime.now()
    # year = str(year) + "0000"



    if request.method == "POST":
        try:
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

            outstanding_bill = request.POST.get('outstanding_bill')

            remarks = request.POST.get('remarks')
            user_type = request.POST.get('user_type')

            assigned_duration = request.POST.get('assigned_duration')
            # renewal_bill = request.POST.get('renewal_bill')
            expiration_bill = request.POST.get('expiration_bill')
            client_id = request.POST.get('client_id')

            # print(expiration_bill)

            install_range = request.POST.get('install_range')
            install_period = request.POST.get('install_period')

            invoice_type = request.POST.get('invoice_type')

            total_amount_due = request.POST.get('total_amount_due')
            outstanding_balance = request.POST.get('outstanding_balance')
            amount_paid = request.POST.get('amount_paid')
            payment_status = request.POST.get('payment_status')
            end_date = request.POST.get('end_date')

            if payment_status == 'full':
                arrears = 0
            else:    
                arrears=request.POST.get('arrears')

            invoice_id = request.POST.get('invoice_id')    

        except:
            print("Something some fields werent passed")   



        assigned = get_object_or_404(AssignPaymentDuration, pk=invoice_id)

        if assigned.deactivate == True:
            if install_range == 'Day(s)':
                    subscription_expiry =  today + datetime.timedelta(days=(int(install_period)))
            elif install_range == 'Month(s)':  
                subscription_expiry =  today + datetime.timedelta(days=(int(install_period) * 30))
            elif install_range == 'Year(s)':    
                subscription_expiry =  today + datetime.timedelta(days=(int(install_period) * 365))
            else:
                subscription_expiry = end_date 
        else:
            subscription_expiry = None 
            


        if int(amount_paid) > int(total_amount_due):
            if int(arrears) <= 0:
                credit= int(amount_paid) - int(total_amount_due)
        else:
            credit = 0     
                

        # url = f"https://db-api-v2.akwaabasoftware.com/members/user/{member_id}"

        # payload = json.dumps({})
        # headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json','Cookie': 'csrftoken=MmSz4Xh2CHMcrgt1chJAlu27V1FZvTjL2KUbJ9nqbaQw3fsCIUeebhhdigNSyZI4; sessionid=qvjnfg4gj0wey2swhm50ws0sy2hnx0az'}

        # person = requests.request("GET", url, headers=headers, data=payload).json()['data']


        # firstname = person['firstname']
        # middlename = person['middlename']
        # surname = person['surname']
        # member_id = person['id']


        # if middlename == "":
        #     username = f"{firstname} {surname}"
        # else:
        #     username = f"{firstname} {middlename} {surname}" 


        make_payments = MakePayment(
                            branch=branch,
                            member_category=member_category,
                            group=group,
                            subgroup=subgroup,
                            member=member,
                            member_id=member_id,
                            client_id=client_id,
                            fee_type=fee_type,
                            fee_description=fee_description,
                            outstanding_bill=outstanding_bill,
    
                            remarks=remarks,
                            user_type=user_type,
                            assigned_duration=assigned_duration,

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
                            invoice_id=invoice_id,
                        )
        make_payments.save()  

        invoice_no = f'FMS{int(year)+make_payments.id}'

        
        make_payments.invoice_no = invoice_no  
        make_payments.save() 


        try:
            base = Currency.objects.get(client_id=client_id, base=True).currency

        except:
            base = "GHS" 

    
        url = "https://manilla.nsano.com/checkout/payment"

        payload = json.dumps({
        "order_id": invoice_no,
        "description": "Fee Payment",
        "amount": amount_paid,
        "currency": base,

        "services": {
            "mobile_money": True,
            "cards": True,
            "bank": True
        },
        

        "return_url": f"https://transactions.akwaabasoftware.com/add-transaction/feePayment/{member_id}/{invoice_no}/1234567890/",
        "cancel_url": "/"
        })


        headers = {
            'Authorization': 'Bearer 300147706867',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()['data']['links']['checkout_url']
        print(response)
        
        return render(request, template_name, {'response': response})

    







def makePayments(request, **kwargs):
    
    template_name = 'client/make-payment.html'
    pk = kwargs.get('pk')
    member_id = kwargs.get('mid')


    try:
        details = MemberDetails.objects.filter(mid=member_id).last()
        member_account_name = details.account_name
        member_branch = details.branch
        mid = details.mid
        token = details.token
        client_id = details.client_id

        try:
            base = Currency.objects.get(client_id=client_id, base=True).currency
            
        except:
            base = 'GHS'    

        try:
            dasho = Dasha.objects.get(mid=mid)

            if dasho.redirected == True:
                setItem = True
            else:
                setItem = False
        except:
            setItem = False  


    except:
        token = ""
        member_account_name = "Demo Account"
        member_branch = "Other Branch"
        mid = 1
        setItem = False
        base = 'GHS'
        client_id = 1

    

    # client_id = MemberDetails.objects.filter(mid=member_id).first().client_id

    assigned = get_object_or_404(AssignPaymentDuration, pk=pk)
    # print(assigned.deactivate == "True")
    organizations = InvoiceDetails.objects.filter(client_id=client_id).first()

    company = InvoiceDetails.objects.all().first()
    date = assigned.end_date.strftime('%Y-%m-%d')
    balance = Balance.objects.all()
    today = datetime.date.today()
    last_paid = datetime.datetime.today().strftime("%Y-%m-%d")
    year = datetime.datetime.now().year
    today = datetime.datetime.now()
    year = str(year) + "0000"


    return render(request, template_name, {
    'assigned': assigned, 
    'dated': date,  
    'period': AssignPeriod.objects.all()[:3],
    'company':organizations,
    'base':base,
    'token': token,
    'member_account_name': member_account_name, 
    'member_branch':member_branch, 
    'mid':mid, 
    'token':token, 
    'setItem': setItem, 
    'base': base, 
    'clid':client_id
    })






def viewPayments(request, **kwargs):

    template_name = 'client/view-payments.html'
    member_id = kwargs.get('mid')
    trans_url = 'https://transactions.akwaabasoftware.com'



    try:
        details = MemberDetails.objects.filter(mid=member_id).last()
        member_account_name = details.account_name
        member_branch = details.branch
        mid = details.mid
        token = details.token
        client_id = details.client_id

        try:
            base = Currency.objects.get(client_id=client_id, base=True).currency
            
        except:
            base = 'GHS'    

        try:
            dasho = Dasha.objects.get(mid=mid)

            if dasho.redirected == True:
                setItem = True
            else:
                setItem = False
        except:
            setItem = False  


    except:
        token = ""
        member_account_name = "Demo Account"
        member_branch = "Other Branch"
        mid = 1
        setItem = False
        base = 'GHS'
        client_id = 1


    try:
        order_id = MakePayment.objects.filter(member_id=member_id).last().invoice_no

        # confirming payment
        url = trans_url + f"/transactions/{order_id}/{member_id}/"
        # print(order_id)
        # print(member_id)



        payload={}
            
        headers = {}

        # paid = requests.request("GET", url, headers=headers, data=payload).json()['data']
        paid = requests.request("GET", url, headers=headers, data=payload).json()['success']
        # print(paid)

        if paid == True:
            status = MakePayment.objects.get(member_id=member_id, invoice_no=order_id)

            if status.confirmed == True:
                pass

            else:
                status.confirmed = True
                status.save()


                payment = TotalPayments(member=status.member, member_id=member_id, client_id=status.client_id, payment=status.amount_paid)
                payment.save()


                # assigned.total_invoice = assigned.total_invoice - int(amount_paid)
                # print(expiration_bill is None)

            assigned = get_object_or_404(AssignPaymentDuration, pk=status.invoice_id)

            if status.expiration_bill is not None:
                if int(status.expiration_bill) > 0:
                    assigned.expiration_bill = int(status.expiration_bill) - int(status.amount_paid)
                    assigned.save()
                else:
                    assigned.expiration_bill = assigned.total_invoice  - int(status.amount_paid)
                    assigned.save()
            else:
                assigned.expiration_bill = assigned.total_invoice  - int(status.amount_paid)
                assigned.save()



                if len(Balance.objects.filter(member=status.member, member_id=member_id)) > 0:
                    balance = Balance.objects.get(member=status.member, member_id=member_id)
                    balance.credit = status.credit
                    balance.save()
                else:
                    balance = Balance(member=status.member, member_id=member_id, credit=status.credit)
                    balance.save()
        
        else:
            pass
      

    except:    
        pass


    payments = MakePayment.objects.filter(member_id=member_id, confirmed=True).order_by('-id')


    return render(request, template_name, {
        'payments': payments,
        'base':base,
        'token': token,
        'member_account_name': member_account_name, 
        'member_branch':member_branch, 
        'mid':mid, 
        'token':token, 
        'setItem': setItem, 
        'base': base, 
        'clid':client_id
    })




def viewDetail(request, **kwargs):
    template_name = 'client/view-detail.html'
    pk = kwargs.get('pk')
    member_id = kwargs.get('mid')



    try:
        details = MemberDetails.objects.filter(mid=member_id).last()
        member_account_name = details.account_name
        member_branch = details.branch
        mid = details.mid
        token = details.token
        client_id = details.client_id

        try:
            base = Currency.objects.get(client_id=client_id, base=True).currency
            
        except:
            base = 'GHS'    

        try:
            dasho = Dasha.objects.get(mid=mid)

            if dasho.redirected == True:
                setItem = True
            else:
                setItem = False
        except:
            setItem = False  


    except:
        token = ""
        member_account_name = "Demo Account"
        member_branch = "Other Branch"
        mid = 1
        setItem = False
        base = 'GHS'
        client_id = 1
 
    payment = get_object_or_404(MakePayment, pk=pk)


    return render(request, template_name, {
        'payment': payment, 
        'base':base,
        'token': token,
        'member_account_name': member_account_name, 
        'member_branch':member_branch, 
        'mid':mid, 
        'token':token, 
        'setItem': setItem, 
        'base': base, 
        'clid':client_id
        })




def viewAssigned(request, **kwargs):
    # if MemberDetails.objects.count() > 0:

        template_name = 'client/view-assigned.html'
        pk = kwargs.get('pk')
        member_id = kwargs.get('mid')


        try:
            details = MemberDetails.objects.filter(mid=member_id).last()
            member_account_name = details.account_name
            member_branch = details.branch
            mid = details.mid
            token = details.token
            client_id = details.client_id

            try:
                base = Currency.objects.get(client_id=client_id, base=True).currency
                
            except:
                base = 'GHS'    

            try:
                dasho = Dasha.objects.get(mid=mid)

                if dasho.redirected == True:
                    setItem = True
                else:
                    setItem = False
            except:
                setItem = False  


        except:
            token = ""
            member_account_name = "Demo Account"
            member_branch = "Other Branch"
            mid = 1
            setItem = False
            base = 'GHS'
            client_id = 1


        assigned = get_object_or_404(AssignPaymentDuration, pk=pk)
        # organizations = get_object_or_404(InvoiceDetails, pk=1)

        organizations = InvoiceDetails.objects.filter(client_id=client_id).first()
        # base = Currency.objects.get(client_id=client_id, base=True).currency


        return render(request, template_name, {
            'assigned': assigned, 
            'organizations': organizations, 
            'base':base,
            'token': token,
            'member_account_name': member_account_name, 
            'member_branch':member_branch, 
            'mid':mid, 
            'token':token, 
            'setItem': setItem, 
            'base': base, 
            'clid':client_id
        })






def delete_payment(request, *args, **kwargs):
    
    if request.method == "POST":
        payment_ids = request.POST.getlist('id[]')

        for payment_id in payment_ids:
            payment = Payments.objects.get(pk=payment_id)
            payment.delete()

        messages.success(request, 'Payment record deleted successfully!')
        return HttpResponseRedirect(reverse('client:viewPayments'))        




# def delete_assigned(request, *args, **kwargs):
#     if request.method == "POST":
#         assigned_ids = request.POST.getlist('id[]')

#         for assigned_id in assigned_ids:
#             assigned = AssignPaymentDuration.objects.get(pk=assigned_id)
#             assigned.delete()

#         messages.success(request, 'Assigned invoice deleted successfully!')
            
#         return HttpResponseRedirect(reverse('client:viewAssignedPayments'))        




# def viewProfile(request):
#     if MemberDetails.objects.count() > 0:
#         template_name = 'client/profile.html'
#         try:
#             holder = Members.objects.get(member=member)
#         except:
#             holder = Members.objects.filter(member=member).first()  

#         # print(expiry)

#         # end = expiry.strftime("%d-%m-%Y")    

#         return render(request, template_name, {'user': user, 'expiry': expiry, 'holder': holder})
#     else:
#         messages.error(request, 'Please Login to continue') 
#         return HttpResponseRedirect(reverse('login:login'))



# def viewDonation(request, **kwargs):
#     if MemberDetails.objects.count() > 0:

#         template_name = 'client/view-donation.html'
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




def payDonation(request, **kwargs):
    if MemberDetails.objects.count() > 0:

        admin = user['firstname'] +' '+ user['surname']
        firstname = user['firstname']
        surname =  user['surname']
        email = user['email']
        phone = user['phone']
        

        template_name = 'client/pay-donation.html'

        pk = kwargs.get('id')
        members = Members.objects.all()
        assigned = get_object_or_404(AssignPaymentDuration, pk=pk)
        company = InvoiceDetails.objects.all().first()
        organizations = get_object_or_404(InvoiceDetails, pk=1)
        # print(organizations.logo)

        
        today = datetime.date.today()
        last_paid = datetime.datetime.today().strftime("%Y-%m-%d")
        year = datetime.datetime.now().year
        today = datetime.datetime.now()
        year = str(year) + "0000"



        if request.method == 'POST':
            
            member = request.POST.get('member')
            donation_name = request.POST.get('donation_name')


            payers_first_name = request.POST.get('payers_first_name')
            payers_last_name = request.POST.get('payers_last_name')
            contact = request.POST.get('contact')
            email_address = request.POST.get('email_address')

            amount_paid = request.POST.get('amount_paid')
    
                
            make_payments = MakePayment(
                            member=member,
                            donation_name=donation_name,
                            payers_first_name=payers_first_name,
                            payers_last_name=payers_last_name,
                            contact=contact,
                            email_address=email_address,
                            amount_paid=amount_paid, 
                            )
            make_payments.save()  

            # invoice_no = f'FMS{year}{month}{day}{make_payments.id}'
            invoice_no = f'FMS{int(year)+make_payments.id}'

            
            make_payments.invoice_no = invoice_no  
            make_payments.save() 


            if len(Members.objects.filter(member=member)) > 0:
                member = Members.objects.get(member=member)
                member.recently_paid = last_paid
                member.save()
            else:
                pass  


            if len(Donation.objects.filter(donation_name=donation_name)) > 0:
                donation = Donation.objects.get(donation_name=donation_name)
                donation.amount_received = int(donation.amount_received) + int(amount_paid)
                donation.save()
            else:
                pass


            try:
                paid_member = Members.objects.get(member=member)
            except:
                paid_member = Members.objects.filter(member=member).first()  


            # Send email
            subject = f'PAID {donation_name}'
            body = f"""
                        Hi {member}, 
                        An amount of GHc {amount_paid} has been paid as {donation_name}. 
                        Many thanks  from {company.company_name}.
                    """
            senders_mail = settings.EMAIL_HOST_USER
            to_address = [f'{email_address}']


            send_mail(subject, body, senders_mail, to_address, fail_silently=False)


            
            company = InvoiceDetails.objects.all().first()
            detail = get_object_or_404(MakePayment, pk=make_payments.id)


            template = get_template('client/donation_printer.txt')
            context = {
                'detail': detail,
                'company': company, 
                }


            message = template.render(context)
            email = EmailMultiAlternatives(subject, message, senders_mail, to_address)
            email.content_subtype = 'html'

            try:
                email.send()
            except: 
                print("Server error")
                pass


            # Send SMS
            message = f"""
                        Hi {member}, 
                        An amount of GHc {amount_paid} has been paid as {donation_name}. 
                        Many thanks  from {company.company_name}.
                    """

            payload= json.dumps({
                        "token": f'{msg}',
                        "message_numbers": [f'{paid_member.contact}'],
                        "message_body": message,
                        "sender_id": "nstacom",
                        "subject": f"Paid {donation_name}",
                        "schedule": f'{today.strftime("%Y-%m-%d %H:%M:%S")}'
                        # "schedule": "2022-06-12 05:30:53"
                })
            files=[]
            headers = { 
                    'Content-Type': 'application/json',
                    'Cookie': 'ci_session=207c8f86bebfac4e513b0558b353015141475c36'
                    }

            response = requests.request("POST", sms_url, headers=headers, data=payload, files=files)
            print(response.text)

            message = Message(sms='sms', message=message, contact=f'{paid_member.contact}')
            message.save()

            messages.success(request, 'Payment made successfully!')

            return HttpResponseRedirect(reverse('superuser:viewPayments')) 
            # return HttpResponseRedirect('/view-payments')        
        else:
  
            return render(request, template_name, {'assigned': assigned, 'organizations':organizations, 'firstname':firstname, 'surname':surname, 'email':email, 'phone':phone,})

    else:
        messages.error(request, 'Please Login to continue') 
        return HttpResponseRedirect(reverse('login:login'))


def viewProfile(request, **kwargs):
    
    template_name =  'client/client-profile.html' 
    member_id = kwargs.get('mid')



    try:
        details = MemberDetails.objects.filter(mid=member_id).last()
        member_account_name = details.account_name
        member_branch = details.branch
        mid = details.mid
        token = details.token
        client_id = details.client_id

        try:
            base = Currency.objects.get(client_id=client_id, base=True).currency
            
        except:
            base = 'GHS'    

        try:
            dasho = Dasha.objects.get(mid=mid)

            if dasho.redirected == True:
                setItem = True
            else:
                setItem = False
        except:
            setItem = False  


    except:
        token = ""
        member_account_name = "Demo Account"
        member_branch = "Other Branch"
        mid = 1
        setItem = False
        base = 'GHS'
        client_id = 1

    
    # print(member_id)
    # url = f'http://api.akwaabaapp.com/members/user?id={member_id}'

    url = f"https://db-api-v2.akwaabasoftware.com/members/user/{member_id}"

    payload = json.dumps({})
    headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json','Cookie': 'csrftoken=MmSz4Xh2CHMcrgt1chJAlu27V1FZvTjL2KUbJ9nqbaQw3fsCIUeebhhdigNSyZI4; sessionid=qvjnfg4gj0wey2swhm50ws0sy2hnx0az'}

    try:
        member = requests.request("GET", url, headers=headers, data=payload).json()['data']
        detail = True
    except:
        member = []
        detail = False    
    # member = requests.request("GET", url, headers=headers, data=payload).json()

    return render(request, template_name, {
        'member': member, 
        'detail':detail,
        'base':base,
        'token': token,
        'member_account_name': member_account_name, 
        'member_branch':member_branch, 
        'mid':mid, 
        'token':token, 
        'setItem': setItem, 
        'base': base, 
        'clid':client_id
        }) 







def logout(request, **kwargs):
    
    member_id = kwargs.get('mid')

    client = MemberDetails.objects.filter(mid=member_id).delete()

    try:
        dasho = Dasha.objects.get(mid=member_id).delete()
    except:
        pass    
    
    # messages.success(request, 'Logged Out Successfully')
    return HttpResponseRedirect(reverse('login:login'))  




# def payOnline(request, *args, **kwargs):
#     if MemberDetails.objects.count() > 0:
#         template_name = 'client/pay-online.html'

#         if request.method == "POST":
#             uid = request.POST.get('uid')
#             pk = kwargs.get('pk')
#             items = []


#             url = f"http://api.akwaabaapp.com/members/user/{uid}"

#             if len(client_email) > 0 and len(client_password) > 0:
#                 payload = json.dumps({ "phone_email": client_email[-1], "password": client_password[-1] })
#                 # print(client_email[-1], client_password[-1])
#             else:
#                 payload = json.dumps({ "phone_email":os.environ.get('LOGIN_EMAIL'), "password": os.environ.get('LOGIN_PASSWORD') })
#                 # print(os.environ.get('LOGIN_EMAIL'), os.environ.get('LOGIN_PASSWORD'))

#             headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json', 'Cookie': 'csrftoken=PmuB7mZ3fXkrs8rg8AG9hT4lirE2iMuHa1ekEEty3Z7pCWZBqIXmqD1b0WXZQzvw; sessionid=ruu6ibfixx18a2o91hvw86jgjrgrg144'}

#             response = requests.request("GET", url, headers=headers, data=payload).json()

#             for item in response.keys():
#                 items.append(item)

#             if "detail" in items:  
#                 messages.error(request, 'Invalid user ID') 
#                 return HttpResponseRedirect(reverse('client:payOnline'))     
#             else:
#                 return HttpResponseRedirect(reverse('client:viewAssignedPayments')) 

#         else:
#             return render(request, template_name, {})
#     else:
#         messages.error(request, 'Please Login to continue') 
#         return HttpResponseRedirect(reverse('login:login'))