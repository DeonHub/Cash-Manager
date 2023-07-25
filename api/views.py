from login.models import ClientDetails, MemberDetails
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.views import APIView
from superuser.models import AssignPaymentDuration, MakePayment, TotalAmount, TotalPayments
from client.models import *
import datetime
import requests
import json
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from django.urls import reverse
import random
import string

import os
import environ
import base64




env = environ.Env()
environ.Env.read_env()


# Create your views here.
def random_char(y):
    return ''.join(random.choice(string.ascii_uppercase) for x in range(y))


class Dashboard(APIView):


    def get(self, request, *args, **kwargs):

        today = datetime.date.today()

        token = kwargs.get('token')
        session_id = request.COOKIES.get('session_id')

        token = base64.b64decode(token).decode("utf-8")
        

        items = []
        base_url = "https://db-api-v2.akwaabasoftware.com/clients"
        url = base_url+"/verify-token"
        payload = json.dumps({ "token": token })

        headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}
        key = requests.request("POST", url, headers=headers, data=payload).json()
        user = requests.request("POST", url, headers=headers, data=payload).json()

        for item in key.keys():
            items.append(item)
        if "non_field_errors" in items:  

            response = HttpResponse("You have been logged out.") 
            response.delete_cookie('session_id')

            messages.error(request, 'Incorrect email or password') 
            return HttpResponseRedirect(reverse('login:login'))     
        else:
            token = key['token']
            userId = user['user']['id']
            account_id = user['user']['accountId']
            branch_id = user['user']['branchId']
            firstname = user['user']['firstname']
            surname = user['user']['surname']
            phone = user['user']['phone']
            email = user['user']['email']
            fullname = f'{firstname} {surname}'
            
            payload = json.dumps({})

            headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json',
            'Cookie': 'csrftoken=L7T0btpjJQY6ui0vF4Q7xZJHRVa4w4ZGwTIDnhrpxekccH2TugoVOGMmvNrc7YsI; sessionid=vtslfhyk77anv2ha7loicgehrj5rafq3'
            }


            account_url = f"{base_url}/account/{account_id}"
            pid = requests.request("GET", account_url, headers=headers, data=payload).json()['data']['id']
            account_name = requests.request("GET", account_url, headers=headers, data=payload).json()['data']['name']


            branch_url =  f"{base_url}/branch/{branch_id}"

            try:
                branch = requests.request("GET", branch_url, headers=headers, data=payload).json()['data']['name']
            except:
                branch = "Main Branch"    



            access_url = f"{base_url}/user-access?userId={userId}"


            access = requests.request("GET", access_url, headers=headers, data=payload).json()['data']
            unlimited = False
        
            for x in access:
                
                if x['pageId']['moduleInfo']['module'] == "Cash Manager":
                    
                    if x['isUnlimited']['name'] == "Unlimited":
                        
                        unlimited = True
            

            try:
                details = ClientDetails.objects.get(session_id=session_id)
                details.pid=pid
                details.account_name = account_name
                details.branch = branch
                details.email = email
                details.phone = phone
                details.token = token
                details.firstname=firstname
                details.surname=surname
                details.fullname=fullname
                details.userId=userId
                details.unlimited=unlimited
                
                details.expiry_date =  today + datetime.timedelta(days=(int(30)))
                details.save()
                
            except:
                details = ClientDetails.objects.create(
                    session_id=session_id,
                    account_name=account_name, 
                    branch=branch, 
                    pid=pid, 
                    token=token, 
                    email=email,
                    firstname=firstname, 
                    fullname=fullname,
                    surname=surname, 
                    phone=phone,
                    userId=userId,
                    unlimited=unlimited
                    )
                details.expiry_date =  today + datetime.timedelta(days=(int(30)))
                details.save()

        
            messages.success(request, 'Login Successful') 
            redirect_url = f"https://cash.akwaabasoftware.com/superuser/"
                   
        return redirect(redirect_url) 










class AssignedFees(APIView):


    def get(self, request, *args, **kwargs):

        today = datetime.date.today()

        token = kwargs.get('token')

        
        items = []
        base_url = "https://db-api-v2.akwaabasoftware.com/members"
        url = base_url+"/verify-token"
        payload = json.dumps({ "token": token })

        headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}

        key = requests.request("POST", url, headers=headers, data=payload).json()
        user = requests.request("POST", url, headers=headers, data=payload).json()


        if "detail" in items: 
            messages.error(request, 'Invalid token') 
       
            redirect_url = "https://cash.akwaabasoftware.com/"
            
            # return redirect('login:login', pid) 

        else:
            token = key['token']
            mid = user['user']['id']
            client_id = user['user']['clientId']


            try:
                details = ClientDetails.objects.get(pid=client_id)
            
                branch = details.branch
                account_name = details.account_name

            except:
                branch = "Main Branch"
                account_name = "Demo Organization" 


            try:
                details = MemberDetails.objects.get(account_name=account_name, branch=branch, mid=mid, client_id=client_id )
                details.expiry_date =  today + datetime.timedelta(days=(int(30)))
                details.save()
            except:
                details = MemberDetails.objects.create(account_name=account_name, branch=branch, mid=mid, client_id=client_id, token=token )
                details.expiry_date =  today + datetime.timedelta(days=(int(30)))
                details.save()
            
            try:
                dasho = Dasha.objects.get(mid=mid)
                dasho.redirected = True
                dasho.save()
            except:
                dasho = Dasha.objects.create(mid=mid, redirected=True)
                dasho.save()
 
            redirect_url = f"https://cash.akwaabasoftware.com/member/{mid}/view-assigned-payments/"   

        
        return redirect(redirect_url) 




class GetMemberTotal(APIView):

    def get(self, request, **kwargs):
        
        member_id = kwargs.get('member_id')


        total_payments = 0
        total_invoice = 0

        try:

            temp_invoice = [int(invoice.total) for invoice in TotalAmount.objects.filter(member_id=member_id)]
            temp_payments = [int(invoice.payment) for invoice in TotalPayments.objects.filter(member_id=member_id)]

            for i in temp_invoice:
                total_invoice += i

            for i in temp_payments:
                total_payments += i

            total_arrears = total_invoice - total_payments 
  

            if total_arrears >= 0:
                pass
            else:
                total_arrears = 0  

            data = {
                # "success": True,
                "total_assigned": "{:,}".format(total_invoice),
                "total_paid": "{:,}".format(total_payments),
                "total_arrears": "{:,}".format(total_arrears)
                }

            return Response(data, status=status.HTTP_200_OK) 

        except:
            error = {
                # "success": True,
                "total_assigned": 0,
                "total_paid": 0,
                "total_arrears": 0

                }

            return Response(error, status=status.HTTP_400_BAD_REQUEST)        





class GetClientTotal(APIView):
    
    def get(self, request, **kwargs):
        
        client_id = kwargs.get('client_id')


        total_payments = 0
        total_invoice = 0

        try:

            temp_invoice = [int(invoice.total) for invoice in TotalAmount.objects.filter(client_id=client_id)]
            temp_payments = [int(invoice.payment) for invoice in TotalPayments.objects.filter(client_id=client_id)]

            for i in temp_invoice:
                total_invoice += i

            for i in temp_payments:
                total_payments += i

            total_arrears = total_invoice - total_payments 
  

            if total_arrears >= 0:
                pass
            else:
                total_arrears = 0  

            data = {
                # "success": True,
                "total_assigned": "{:,}".format(total_invoice),
                "total_paid": "{:,}".format(total_payments),
                "total_arrears": "{:,}".format(total_arrears)
                }

            return Response(data, status=status.HTTP_200_OK) 

        except:
            error = {
                # "success": True,
                "total_assigned": 0,
                "total_paid": 0,
                "total_arrears": 0

                }

            return Response(error, status=status.HTTP_400_BAD_REQUEST)        




class GetFeeTypes(APIView):
    
    def get(self, request, **kwargs):

        client_id = kwargs.get('client_id')
        
        subscribers = FeeType.objects.filter(client_id=client_id)
        all_type = FeeTypeSerializer(subscribers, many=True)

        return Response(all_type.data)



class GetFeeDescriptions(APIView):
    
    def get(self, request, **kwargs):

        client_id = kwargs.get('client_id')

        subscribers = FeeDescription.objects.filter(client_id=client_id)
        all_type = FeeDescriptionSerializer(subscribers, many=True)
        return Response(all_type.data)


class GetPeriods(APIView):
    
    def get(self, request, **kwargs):

        subscribers = AssignPeriod.objects.all()
        all_type = PeriodSerializer(subscribers, many=True)
        return Response(all_type.data)



class GetAmountDue(APIView):

    def get(self, request, **kwargs):
        # template_name = 'superuser/amount_due.html'

        if request.method == 'GET': 
            assigned_id = kwargs.get('id')
            assigned_range = kwargs.get('range')
            assigned_period = kwargs.get('period')


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


            user_history = {
                "amount": total_amount_due
            }
            
            return Response(user_history) 


class GetCredit(APIView):

    def get(self, request, **kwargs):
        # template_name = 'superuser/credit.html'

        if request.method == 'GET': 
            # member = kwargs.get('member')
            member_id = request.GET.get('member_id')

            try:
                credit = Balance.objects.filter(member_id=member_id).credit
            except:
                credit = 0    

            user_history = {
                "credit": credit
            }
            
            return Response(user_history) 




# class SetEmailDetails(APIView):
    
#     def post(self, request, *args):

#         today = datetime.date.today()
#         year = datetime.datetime.now().year
#         year = str(year) + "0000"

#         members = EmailSerializer(data=request.data)

#         if members.is_valid():
#             client_id = members.data['client_id']
#             branch = members.data['branch']
#             email = members.data['email']
#             password = members.data['password']

#             client_emails = ClientEmails.objects.create( client_id=client_id, branch=branch, email=email, password=password )
#             client_emails.save()

#             data = {
#                 "success": True,
#                 "msg": "Client email set successfully",
#              }

#             return Response(data, status=status.HTTP_200_OK)
#         else:
#             return Response(members.errors, status=status.HTTP_400_BAD_REQUEST)  





class GetPaymentLink(APIView):


    def post(self, request, *args, **kwargs):

        today = datetime.datetime.today()
        now = datetime.datetime.now()
        year = datetime.datetime.now().year
        # today = datetime.datetime.now()
        year = str(year) + "0000"

        members = PaymentSerializer(data=request.data)

       
        if members.is_valid():

            branch = members.data['branch']
            member_category = members.data['member_category']
            group = members.data['group']
            subgroup = members.data['subgroup']
            member = members.data['member']
            member_id = members.data['member_id']
            code = members.data['code']
            invoice_type = members.data['invoice_type']
            platform = members.data['platform']
            

            fee_type_id = members.data['fee_type_id']
            fee_type = FeeType.objects.get(id=fee_type_id) 

            fee_description_id = members.data['fee_description_id']
            fee_description = FeeDescription.objects.get(id=fee_description_id) 


            fee_type_value = fee_type.fee_type
            fee_description_value = fee_description.fee_description

            outstanding_bill = members.data['outstanding_bill']

            remarks = members.data['remarks']
            # user_type = members.data['user_type']

            assigned_duration = members.data['assigned_duration']
            # renewal_bill = request.POST.get('renewal_bill')
            expiration_bill = members.data['expiration_bill']
            client_id = members.data['client_id']

            # print(expiration_bill)

            install_range = members.data['install_range']
            install_period = members.data['install_period']


            

            total_amount_due = members.data['total_amount_due']
            outstanding_balance = members.data['outstanding_balance']
            amount_paid = members.data['amount_paid']
            payment_status = members.data['payment_status']
            # print(payment_status)


            end_date = members.data['end_date']

            if payment_status == 'full':
                arrears = 0
            else:    
                arrears=members.data['arrears']

            invoice_id = members.data['invoice_id']    



            assigned = get_object_or_404(AssignPaymentDuration, pk=invoice_id)

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

                                fee_type_value=fee_type_value,
                                fee_description_value=fee_description_value,

                                invoice_type=invoice_type,
                                remarks=remarks,
                                # user_type=user_type,
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


        
            url = "https://payproxyapi.hubtel.com/items/initiate"
            
            if platform == 'unaapp':
                returnUrl = f"https://unaapp.org/payfees/{code}/{member_id}/view-payments/{client_id}/"
                # returnUrl = f"http://127.0.0.1:5000/payfees/{code}/{member_id}/view-payments/{client_id}/"
            else:
                returnUrl = f"https://tuakaonline.com/payfees/{code}/{member_id}/view-payments/{client_id}/"
                # returnUrl = f"http://127.0.0.1:5000/payfees/{code}/{member_id}/view-payments/{client_id}/"


            payload = json.dumps({
                    "totalAmount": amount_paid,
                    "description": "Fees Payment",
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

            user_history = {
                "link": response
            }
            
            
            return Response(user_history, status=status.HTTP_200_OK)
        else:
            return Response(members.errors, status=status.HTTP_400_BAD_REQUEST)  



    


class GetHistory(APIView):

    def get(self, request, **kwargs):
        
        member_id = kwargs.get('mid')
        client_id = kwargs.get('pid')
        trans_url = 'https://transactions.akwaabasoftware.com'


        try:
            order_id = MakePayment.objects.filter(member_id=member_id).last().invoice_no

            # confirming payment
            url = f"{trans_url}/transactions/{order_id}/"

            payload = {}
                
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


                status.amount_left = int(assigned.expiration_bill)  
                status.save()   


                try:
                    balance = Balance.objects.get(member=status.member, member_id=member_id)
                    balance.credit = status.credit
                    balance.save()
                except:
                    balance = Balance(member=status.member, member_id=member_id, credit=status.credit)
                    balance.save()



                try:
                    online = OnlinePayments.objects.get(client_id=client_id, branch=status.branch, member_category=status.member_category, group=status.group, subgroup=status.subgroup)
                    online.total += float(status.amount_paid)
                    online.save()
                except:
                    online = OnlinePayments.objects.create(client_id=client_id, total=status.amount_paid, branch=status.branch, member_category=status.member_category, group=status.group, subgroup=status.subgroup)
                    online.save()

    


                # if len(Balance.objects.filter(member=status.member, member_id=member_id)) > 0:
                #     balance = Balance.objects.get(member=status.member, member_id=member_id)
                #     balance.credit = status.credit
                #     balance.save()
                # else:
                #     balance = Balance(member=status.member, member_id=member_id, credit=status.credit)
                #     balance.save()
            
            else:
                pass
        
        except:    
            pass


        payments = MakePayment.objects.filter(member_id=member_id, client_id=client_id, confirmed=True).order_by('-id')
        
        heroes = HistorySerializer(payments, many=True)

        user_history = {
            "data": heroes.data
        }
        
        return Response(user_history)








class GetAssignedFees(APIView):



    def get(self, request, **kwargs):
        all_payments = AssignPaymentDuration.objects.all()

        member_id = self.request.query_params.get('member_id', None)
        client_id = self.request.query_params.get('client_id', None)
        usercode = self.request.query_params.get('usercode', None)


        if member_id:
            all_payments = AssignPaymentDuration.objects.filter(member_id=member_id)


        if client_id:
            all_payments = AssignPaymentDuration.objects.filter(client_id=client_id)


        if usercode:
            all_payments = AssignPaymentDuration.objects.filter(usercode=usercode)


        heroes = AssignPaymentDurationSerializer(all_payments, many=True)

        user_history = {
            "count": len(all_payments),
            "data": heroes.data
        }
        
        return Response(user_history)








class ValidateCode(APIView):
    
    def get(self, request, **kwargs):
        
        usercode = kwargs.get('usercode')

        try:
            code = Usercode.objects.get(usercode=usercode)
            
            user_history = {
                "success": "True",
            }
            
            return Response(user_history, status=status.HTTP_200_OK)
   
        except:
            error = {
                "success": "False",
                }

            return Response(error, status=status.HTTP_400_BAD_REQUEST)  













class GetAssignedFeesById(APIView):
    
    def get(self, request, **kwargs):
        
        aid = kwargs.get('aid')

        try:
            all_payments = AssignPaymentDuration.objects.get(pk=aid)
        
            heroes = AssignPaymentDurationSerializer(all_payments)

            user_history = {
                "data": heroes.data
            }
            
            return Response(user_history, status=status.HTTP_200_OK)

        except:
            error = {

                "data": []
                }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)  




  

class GetAssignedFeesByCode(APIView):

    def get(self, request, **kwargs):
        
        usercode = kwargs.get('usercode')
        client_id = kwargs.get('client_id')

        try:
            all_payments = AssignPaymentDuration.objects.filter(usercode=usercode, client_id=client_id)
            
            if len(all_payments) > 0:

                heroes = AssignPaymentDurationSerializer(all_payments, many=True)

                user_history = {
                    "success": True,
                    "count": len(all_payments),
                    "data": heroes.data
                }
                
                return Response(user_history, status=status.HTTP_200_OK)


            else:

                error = {
                    "success": True,
                    "count": 0,
                    "data": []
                    }

                return Response(error, status=status.HTTP_400_BAD_REQUEST)      


        except:
            error = {
                "success": False,
                "count": 0,
                "data": []
                }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)  









class GetBreakdown(APIView):


    def get(self, request, **kwargs):
            
        assigned_id = kwargs.get('assigned_id')

        try:
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


            user_history = {
                    "data": data
                }
                
            return Response(user_history, status=status.HTTP_200_OK)

        except:
            error = {
                "data": []
                }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)  

    

class GetMember(APIView):

    def get(self, request, **kwargs):
            
        usercode = kwargs.get('usercode')

        try:
            user = Usercode.objects.get(usercode=usercode)

            heroes = MemberCodeSerializer(user)

            user_history = {
                "success": True,
                "data": heroes.data
            }
            
            return Response(user_history)

        except:
            error = {
                "success": False,
                "data": []
                }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)  





class GetBaseCurrency(APIView):


    def get(self, request, **kwargs):
            
        client_id = kwargs.get('client_id')

        try:
            base = Currency.objects.get(client_id=client_id, base=True).currency

            user_history = {
                "base": base
            }
            
            return Response(user_history)
        except:
            error = {
                "base": "GHS"
                }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)  




class GetClientDetails(APIView):


    def get(self, request, **kwargs):
            
        client_id = kwargs.get('client_id')

        try:

            details = InvoiceDetails.objects.filter(client_id=client_id).first()
            heroes = ClientDetailsSerializer(details)

            user_history = {
                "success": True,
                "data": heroes.data
            }
            
            return Response(user_history)

        except:

            error = {
                "success": False,
                "data": []
                }

            return Response(error, status=status.HTTP_400_BAD_REQUEST)  

    


class GetClients(APIView):


    def get(self, request, **kwargs):
            
        usercode = kwargs.get('usercode')
        

        try:
            member_id = Usercode.objects.get(usercode=usercode).member_id
            client_id = Usercode.objects.get(usercode=usercode).client_id
            

            token = ClientDetails.objects.get(pid=client_id).token


            clients = list({x.client_id for x in AssignPaymentDuration.objects.filter(member_id=member_id)})
            
            # print(clients)

            user_history = {
                "success": True,
                "token": token,
                "data": clients
            }

            # print(user_history)
            
            return Response(user_history, status=status.HTTP_200_OK)

        except:
            error = {
                "success": False,
                "token": "",
                "data": []
                }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)  

    






class GetPaymentHistory(APIView):

    def get(self, request, **kwargs):
                                         
        all_payments = MakePayment.objects.filter(confirmed=True).order_by('-id')
        member_id = self.request.query_params.get('member_id', None)
        client_id = self.request.query_params.get('client_id', None)
        fee_type = self.request.query_params.get('fee_type', None)
        fee_description = self.request.query_params.get('fee_description', None)
        fee_type_value = self.request.query_params.get('fee_type_value', None)
        fee_description_value = self.request.query_params.get('fee_description_value', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if member_id:
            all_payments = MakePayment.objects.filter(member_id=member_id, confirmed=True).order_by('-id')


        if client_id:
            all_payments = MakePayment.objects.filter(client_id=client_id, confirmed=True).order_by('-id')


        if fee_type:
            all_payments = MakePayment.objects.filter(fee_type=fee_type, confirmed=True).order_by('-id')


        if fee_description:
            all_payments = MakePayment.objects.filter(fee_description=fee_description, confirmed=True).order_by('-id')


        if fee_type_value:
            all_payments = MakePayment.objects.filter(fee_type_value=fee_type_value, confirmed=True).order_by('-id')


        if fee_description_value:
            all_payments = MakePayment.objects.filter(fee_description_value=fee_description_value, confirmed=True).order_by('-id')


        if start_date and end_date:
            date_format = '%d-%m-%Y'
            start_date = datetime.datetime.strptime(start_date, date_format)
            end_date = datetime.datetime.strptime(end_date, date_format)
            end_date = end_date+datetime.timedelta(days=1)
            all_payments = MakePayment.objects.filter(date_created__range=[start_date, end_date], confirmed=True).order_by('-id')

        heroes = PaymentHistorySerializer(all_payments, many=True)

        user_history = {
            "count": len(all_payments),
            "data": heroes.data
        }
        
        return Response(user_history)





class GetAccountExpiry(APIView):

    def get(self, request, **kwargs):
        
        member_id = kwargs.get('member_id')

        try:
            all_payments = MakePayment.objects.filter(member_id=member_id, confirmed=True).last()
            expiry_date = all_payments.subscription_expiry


            user_history = {
                # "success": True,
                "account_expiry": expiry_date
            }
            
            return Response(user_history)

        except:
            error = {
                "account_expiry": None
                }
            return Response(error) 




class GetOutstandingBill(APIView):

    
    def get(self, request, **kwargs):

        member_id = kwargs.get('member_id')
        end = datetime.datetime.now().year
        total_bill = 0.00



        try:
            bills = [x.expiration_bill for x in AssignPaymentDuration.objects.filter(member_id=member_id, invoice_type='expiry')]

            for x in bills:
                total_bill += int(x)

            total_bill = "{:,}".format(total_bill)    

            start = AssignPaymentDuration.objects.filter(member_id=member_id, invoice_type='expiry').first().date_created.year  

            user_history = {
                "total_bill": total_bill,
                "start": start,
                "end": end,
            }
            
        except:

            user_history = {
                "total_bill": total_bill,
                "start": 2020,
                "end": end,
            }
            
        return Response(user_history)



class PayOutstandingBill(APIView):

    
    def post(self, request, *args, **kwargs):

        today = datetime.date.today()
        now = datetime.datetime.now()
        year = datetime.datetime.now().year
        # today = datetime.datetime.now()
        year = str(year) + "0000"

        members = OutstandingBillPaymentSerializer(data=request.data)

       
        if members.is_valid():

            member_id = members.data['member_id']

            data = AssignPaymentDuration.objects.filter(member_id=member_id, invoice_type='expiry')

            try:
                for x in data:
                    x.expiration_bill = 0
                    x.save()

                user_history = {
                    "success": True,
                }

            except:
                user_history = {
                    "success": False,
                }  

            return Response(user_history)  

        else:
            return Response(members.errors, status=status.HTTP_400_BAD_REQUEST)               

            





class AutoAssign(APIView):

    def post(self, request, *args, **kwargs):


        today = datetime.date.today()
        now = datetime.datetime.now()
        year = datetime.datetime.now().year
        year = str(year) + "0000"

        members = AutoAssignSerializer(data=request.data)

       
        if members.is_valid():

            branch = members.data['branch']
            member_category = members.data['member_category']
            group = members.data['group']
            subgroup = members.data['subgroup']
            member = members.data['member']
            email = members.data['email']
            client_id = members.data['client_id']
            member_id = members.data['member_id']

            # date_format = '%d-%m-%Y'
            # date_created = members.data['date_created']
            # date_created = datetime.datetime.strptime(date_created, date_format)

            try:
                company_name = InvoiceDetails.objects.filter(client_id=client_id).first().company_name
            except:
                company_name = "Client Service Alert"    

            token = ClientDetails.objects.get(pid=client_id).token 

            payload = json.dumps({})

            headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json',
            'Cookie': 'csrftoken=yNDF0QM5CW2QBNy2NUMketfGhkwuR4jkCRaHylrYm1HRZ7AICGwYZ39CKkjzEXue; sessionid=7w7fqr0htni2s8f3koi883t715guq8kb'
            }

            try:
                try:
                    assigned = AssignPaymentDuration.objects.filter(client_id=client_id, branch__exact=branch, member_category__exact=member_category, group__exact=group, subgroup__exact=subgroup).last()
                except:
                    try:
                        assigned = AssignPaymentDuration.objects.filter(client_id=client_id, branch__exact=branch, member_category__exact=member_category, group__exact=group).last()
                    except:
                        assigned = AssignPaymentDuration.objects.filter(client_id=client_id, branch__exact=branch, member_category__exact=member_category).last()
   

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

                    membercode = Usercode.objects.create(member_id=member_id, member=member, client_id=client_id, usercode=usercode)  
                    membercode.save()         
            


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
            


                assignPayments = AssignPaymentDuration(
                                    branch = branch,
                                    member_category = member_category,
                                    group = group,
                                    subgroup = subgroup,
                                    member = member,
                                    client_id = client_id,
                                    member_id = member_id,
                                    usercode=usercode,
                                    fee_type = assigned.fee_type,
                                    fee_description = assigned.fee_description,
                                    total_invoice = assigned.total_invoice,
                                    expiration_bill = assigned.total_invoice,
                                    install_range = assigned.install_range,
                                    install_period = assigned.install_period,
                                    end_date = assigned.end_date,
                                    auto=True,
                                    invoice_type= assigned.invoice_type,
                                    amount_by_days= assigned.amount_by_days,
                                 )

                assignPayments.save()


                total = TotalAmount(member=member, member_id=member_id, client_id=client_id, total=assigned.total_invoice)
                total.save()


                if assignPayments.auto == True:
                    pass

                

                # Send email
                subject = f'ASSIGNED BILL/INVOICE'
                message = f"""
                            Hello {member}, 
                            Your new or updated invoice/bill from {company_name}. 
                            Go to https://unaapp.org/ and sign up to get an ACCESS CODE 
                            or login if you already have an access code for payment.
                            Many thanks from {company_name}.
                        """
                from_email = EMAIL_HOST_USER
                to_address = [f'{email}']



                email = EmailMessage(subject, message, from_email, to_address)

                try:
                    email.send()
                    # pass
                except: 
                    print("Server error")
                    pass

                
                # subject = 'Subject of the Email'
                # message = 'Body of the Email'
                # from_email = 'your_email@gmail.com'
                # recipient_list = ['recipient_email@example.com']

                # print(send_mail(subject, message, from_email, to_address, fail_silently=False))

                # try:
                #     send_mail(subject, message, from_email, to_address, fail_silently=False)
                # except: 
                #     print("Server error")
                #     pass


            except:
                pass    


            user_history = {
                "success": True,
                "message": "Fee Assigned Successfully!"
            }  

            return Response(user_history)  

        else:
            return Response(members.errors, status=status.HTTP_400_BAD_REQUEST)      

            

class SendPaymentMail(APIView):

    def get(self, request, *args, **kwargs):

        member_id = kwargs.get('member_id')
        client_id = Usercode.objects.get(member_id=member_id).client_id

        token = ClientDetails.objects.get(pid=client_id).token 
        payment = MakePayment.objects.filter(member_id=member_id).last()


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


        url = f"https://db-api-v2.akwaabasoftware.com/members/user/{member_id}"

        payload = json.dumps({})
        headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json','Cookie': 'csrftoken=MmSz4Xh2CHMcrgt1chJAlu27V1FZvTjL2KUbJ9nqbaQw3fsCIUeebhhdigNSyZI4; sessionid=qvjnfg4gj0wey2swhm50ws0sy2hnx0az'}

        person = requests.request("GET", url, headers=headers, data=payload).json()['data']
        email = person['email']
 

        # Send email
        subject = f'PAID {payment.fee_type}'
        body = f"""
                    Hi {payment.member}, 
                    An amount of GHc {payment.amount_paid} has been paid as {payment.payment_status} payment for {payment.fee_description}. 
                    The outstanding bill is {payment.arrears}. 
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




        company = InvoiceDetails.objects.filter(client_id=client_id).first()
        detail = get_object_or_404(MakePayment, pk=payment.id)

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


        user_history = {
            "success": True,
            "message": "Fee Assigned Successfully!"
        }  

        return Response(user_history)  





class UpdateUserCode(APIView):
    
    def post(self, request, *args, **kwargs):

        members = UsercodeSerializer(data=request.data)
       
        if members.is_valid():
            
            member_id = members.data['member_id']
            usercode = members.data['usercode']

            # print(member_id)
            # print(usercode)

            try:
                assigned = AssignPaymentDuration.objects.filter(member_id=member_id)

                for user in assigned:
                    user.usercode=usercode
                    user.save()

                usercodex = Usercode.objects.get(member_id=member_id)
                
                # for codex in usercodex:
                usercodex.usercode=usercode
                usercodex.save()


                user_history = {
                    "success": True,
                    "message": "Usercode added/updated Successfully!"
                }  

                return Response(user_history) 
                 
            except:

                user_history = {
                    "success": False,
                    "message": "Failed to add!"
                }  

                return Response(user_history)     

        else:
            return Response(members.errors, status=status.HTTP_400_BAD_REQUEST) 
