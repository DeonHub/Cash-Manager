# from fee_sys.requests import count, organization_name, unlimited
# from fee_sys.login import user,client_branch

import datetime
from django.shortcuts import redirect
import requests
import json

from .models import *
import environ

env = environ.Env()
environ.Env.read_env()


    

def counter(request):

    now = datetime.datetime.now()
    year = now.year

    date = now.strftime("%A, %d %B, %Y")

    time = now.strftime("%H:%M %p")

    # print(client_name)
    # print(unlimited)
    

    # return {'total_members': total_members, 'client_name': client_name, 'organization': organization, 'branch':branch, 'unlimited': unlimited, 'date': date, 'time': time, 'year':year, 'new_id':new_id}
    return { 'date': date, 'time': time, 'year':year }




def checkSession(request):

    try:
        request.COOKIES.get('session_id')
    except:    
        return redirect('login:login') 










def getMemberDetails(request):

    # print("Hello, world!")
    namex = ""
    

    return { 'namex': namex }

