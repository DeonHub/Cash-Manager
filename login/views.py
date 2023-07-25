from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.urls import reverse

import requests
import json
import io
import os
from .models import *
from superuser.models import AssignPaymentDuration, MakePayment
import datetime
from itertools import chain
# from django.conf import settings


# Create your views here.


def logins(request):
    template_name = 'login/logins.html'

    return render(request, template_name, {

    })

def index(request):
    template_name = 'login/index.html'

    return render(request, template_name, {

    })


def login(request):

        template_name = 'login/login.html'
        today = datetime.date.today()
        base_url = "https://db-api-v2.akwaabasoftware.com/clients"
        
        if request.method == "POST":
            role = "admin"
            email = request.POST.get('email')
            password = request.POST.get('password')
            session_id = request.COOKIES.get('session_id')


        # clickcomgh@gmail.com,
        # password: password2

            if role == "admin":

                # details = ClientDetails( email=email, password=password)
                # details.save()
                
                items = []
                url = base_url+"/login"
                payload = json.dumps({"phone_email": email, "password": password})
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
                        details.password = password
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
                            password=password, 
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
                    return redirect('superuser:index') 







































            # else:

            #     items = []
            #     url = "https://db-api-v2.akwaabasoftware.com/members/login"
            #     payload = json.dumps({"phone_email": email, "password": password, "checkDeviceInfo": "on", "systemDevice": "1", "deviceType": "1", "deviceId": "1"})
            #     headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}
            #     key = requests.request("POST", url, headers=headers, data=payload).json()
            #     user = requests.request("POST", url, headers=headers, data=payload).json()

            #     for item in key.keys():
            #         items.append(item)

            #     if "non_field_errors" in items:  
            #         messages.error(request, 'Incorrect email or password') 
            #         return HttpResponseRedirect(reverse('login:login'))   

            #     else: 
            #         token = key['token']
            #         mid = user['user']['id']

            #         client_id = user['user']['clientId']
            #         # info = ClientDetails.objects.get(pid=client_id)
            #         # print(info)
            #         # branch = info.branch
            #         # account_name = info.account_name

            #         # print(branch)
            #         # print(account_name)


            #         try:
            #             details = LogDetails.objects.filter(pid=client_id).first()
                    
            #             branch = details.branch
            #             account_name = details.account_name

            #         except:
            #             branch = "Main Branch"
            #             account_name = "Demo Organization" 



            #         # payload = json.dumps({})

            #         # headers = {
            #         # 'Authorization': f'Token {token}',
            #         # 'Content-Type': 'application/json',
            #         # 'Cookie': 'csrftoken=L7T0btpjJQY6ui0vF4Q7xZJHRVa4w4ZGwTIDnhrpxekccH2TugoVOGMmvNrc7YsI; sessionid=vtslfhyk77anv2ha7loicgehrj5rafq3'
            #         # }


            #         # account_url = f"{base_url}/account/{account_id}"
            #         # mid = requests.request("GET", account_url, headers=headers, data=payload).json()['data']['id']
            #         # account_name = requests.request("GET", account_url, headers=headers, data=payload).json()['data']['name']


            #         # branch_url =  f"{base_url}/branch/{branch_id}"

            #         # try:
            #         #     branch = requests.request("GET", branch_url, headers=headers, data=payload).json()['data']['name']
            #         # except:
            #         #     branch = "Main Branch"    



            #         try:
            #             details = MemberDetails.objects.get(account_name=account_name, branch=branch, mid=mid, client_id=client_id, email=email, password=password)
            #             details.expiry_date =  today + datetime.timedelta(days=(int(30)))
            #             details.save()
            #         except:
            #             details = MemberDetails.objects.create(account_name=account_name, branch=branch, mid=mid, client_id=client_id, token=token, email=email, password=password)
            #             details.expiry_date =  today + datetime.timedelta(days=(int(30)))
            #             details.save()
                    

            #         # user = True
            #         messages.success(request, 'Login Successful') 
            #         return redirect('client:index', mid) 

                        
        else:               
            return render(request,  template_name)
      