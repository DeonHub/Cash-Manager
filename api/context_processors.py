# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework import status
# from .serializers import *
# from .models import *
# from rest_framework.views import APIView
# from superuser.models import *
# from client.models import *
# from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.core.files.storage import FileSystemStorage
# from django.shortcuts import redirect, render, get_object_or_404
# from django.contrib import messages
# from django.conf import settings
# from django.urls import reverse
# from fee_sys.requests import *
# from fee_sys.auth import *
# import requests
# import json
# import io
# import os
# from .models import *
# from superuser.models import AssignPaymentDuration, MakePayment
# import datetime
# from itertools import chain

# # import requests

# # Create your views here.

# @api_view(['POST'])
# def log(request):

#     members = LoginSerializer(data=request.data)
    
#     today = datetime.date.today()

#     if members.is_valid():
#         email = members.data['email']
#         password = members.data['password']

#         items = []
#         url = "https://db-api-v2.akwaabasoftware.com/members/login"
#         payload = json.dumps({"phone_email": email, "password": password, "checkDeviceInfo": False})
#         headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}
#         key = requests.request("POST", url, headers=headers, data=payload).json()
#         user = requests.request("POST", url, headers=headers, data=payload).json()

#         for item in key.keys():
#             items.append(item)

#         if "non_field_errors" in items:  
#             pass  

#         else: 
#             token = key['token']

#             new_token = Token.objects.all()
#             if len(new_token) > 0:
#                 new_token.delete()

#             tokenise = Token.objects.create(token=token)  
#             tokenise.save()  

#             member_id = user['id']

#             # Getting the client
#             url = f"https://db-api-v2.akwaabasoftware.com/members/user/{member_id}"
#             payload = json.dumps({ "phone_email":email, "password": password, "checkDeviceInfo": False })

#             headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json', 'Cookie': 'csrftoken=PmuB7mZ3fXkrs8rg8AG9hT4lirE2iMuHa1ekEEty3Z7pCWZBqIXmqD1b0WXZQzvw; sessionid=ruu6ibfixx18a2o91hvw86jgjrgrg144'}

#             response = requests.request("GET", url, headers=headers, data=payload).json()['data']


#             firstname = response['firstname'] 
#             middlename = response['middlename']
#             surname = response['surname']

#             if middlename != '':
#                 name = f'{firstname} {middlename} {surname}'
#             else: 
#                 name = f'{firstname} {surname}'  

#             try:
#                 desks = MakePayment.objects.filter(member=name)
#             except:
#                 pass  


#             for x in desks:  
#                 try:
#                     if x.subscription_expiry < today:
#                         # return Response(members.data)
#                         # account deactivated
#                         pass 
                         
#                     else:
#                         return Response(members.data) 
#                 except:
#                     pass  
        
#     else:
#         return Response(members.errors, status=status.HTTP_400_BAD_REQUEST)  

