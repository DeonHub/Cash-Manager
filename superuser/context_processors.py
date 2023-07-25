# from fee_sys.requests import unlimited
# from fee_sys.login import user,client_branch

from datetime import datetime

from django.shortcuts import redirect


# super_unlimited=unlimited
unlimited = "True"

def period(request):
    if request.method == "GET":
        period = request.GET.get('period')

    return period    

    

def counter(request):

    now = datetime.now()
    year = now.year

    date = now.strftime("%A, %d %B, %Y")

    time = now.strftime("%H:%M %p")

    # print(client_name)
    # print(unlimited)
    

    return { 'date': date, 'time': time, 'year':year }


# def checkSession(request):
    
#     session_id = request.COOKIES.get('session_id')

#     if not session_id:
#         return redirect('login:login') 
#     else:
#         pass
    
    