# import json
# # from pytz import country_names
# import requests
# from login.models import ClientDetails
# # from superuser.models import Members, Count, ClientCount, Clients, User
# # from superuser.context_processors import super_unlimited
# import environ

# env = environ.Env()
# environ.Env.read_env()



# try:
#     detail = ClientDetails.objects.all().last()
#     payload = json.dumps({ "token": detail.token })
# except:
#     payload = json.dumps({ "phone_email": env('LOGIN_EMAIL'), "password": env('LOGIN_PASSWORD'), "checkDeviceInfo": False })



# headers = {
#   'Authorization': f'Token {token}',
#   'Content-Type': 'application/json',
#   'Cookie': 'csrftoken=Ly8oYWb8c70C2CDUYfFd0poVjCL91Octs99w3q6rGjSu8L2SaPVDoGPvJ4tKQIda; sessionid=4zyr1pvz9r6hyu8sqvuh0gqqxsymo56n'
# }


# login_headers = {
#   'Content-Type': 'application/json',
#   'Cookie': 'csrftoken=cMrEAoqAfPVtpPCRsc5EW8MNg7GuNMukbCI1VKL8MjTaxV5VsM5lboltWF0Pv9sp; sessionid=oqefvhuzbfzgbhxev9ih3g2mca6p9x10'
# }


# base_url = "https://db-api-v2.akwaabasoftware.com"
# mail_url = "https://app.nstacom.com"

# # URLS
# login_url = base_url + "/clients/login"

# member_category_url = base_url + "/members/groupings/member-category"
# group_url = base_url + "/members/groupings/group"
# subgroup_url = base_url + "/members/groupings/sub-group"




# # sms_url = mail_url + "/api/compose/sms"
# # voice_url = mail_url + "/api/compose/voice"
# # token_url = mail_url + "/api/compose/generate_token"
# # balance_url = mail_url + "/cronjobs/balances"




# # clients_url = base_url + "/clients/user"
# # url=clients_url 
# # payload = payload
# # headers = headers
# # clients = requests.request("GET", url, headers=headers, data=payload).json()['results']
# # print(clients)
# # client_count = requests.request("GET", url, headers=headers, data=payload).json()['count']
# # print(client_count)




# # members_url = base_url + f"/members/user?clientId={account_id}"
# # # else:   
# # #     members_url = base_url + f"/members/user?clientId={account_id}&branchId={branch_id}"


# # url = members_url
# # payload = payload
# # headers = headers
# # members = requests.request("GET", url, headers=headers, data=payload).json()['results']
# # # print(members)
# # count = requests.request("GET", url, headers=headers, data=payload).json()['count']




# # start = Count.objects.get(id=1)
# # starter = ClientCount.objects.get(id=1)
# # # print(starter.count)

# # # if int(start.count) != int(count) or int(starter.count) != int(client_count):
# # if int(start.count) < int(count):
# #     start.count = int(count)
# #     start.save()

# #     pages = []
# #     if (int(count) // 10) >= 0:
# #         counter = (int(count) // 10) + 1
# #     else:
# #         counter = (int(count) // 10)


# #     for i in range(1, counter+1):
# #         url = base_url + f"/members/user?page={i}"
# #         payload = payload
# #         headers = headers
# #         members = requests.request("GET", url, headers=headers, data=payload).json()['results']

# #         if members not in pages:
# #             pages.append(members)

# #     pages = ([x for xs in pages for x in xs])
    
# #     for x in pages:
# #         member_id = x['id']    
# #         firstname = x['firstname'] 
# #         middlename = x['middlename'] 
# #         surname = x['surname'] 

# #         if middlename == '':
# #                 fullname = f'{firstname} {surname}'
# #         else:
# #                 fullname = f'{firstname} {middlename} {surname}'      

# #         profile_url = x['profilePicture'] 
# #         contact = x['phone'] 
# #         email_address = x['email'] 
# #         level = x['level'] 
# #         status = x['status'] 
# #         member_type = x['memberType'] 
# #         account_type = x['accountType'] 
# #         branch = x['branchId'] 

# #         if len(Members.objects.filter(member_id=member_id)) > 0:
# #             pass  
# #         else:
# #             holders = Members(member_id=member_id, member=fullname, profile_url=profile_url, contact=contact, email_address=email_address, level=level, status=status, member_type=member_type, account_type=account_type, branch=branch)
# #             holders.save() 

# #     print("Success")                


#     # elif int(starter.count) < int(client_count):
#     #     # starter.count = int(client_count)
#     #     # starter.save()
#     #     # print(starter.count)

#     #     pages = []
#     #     if (int(client_count) // 10) >= 0:
#     #         counter = (int(client_count) // 10) + 1
#     #     else:
#     #         counter = (int(client_count) // 10)

#     #     # print(counter)    

#     #     for i in range(1, counter+1):
#     #         url = base_url + f"/clients/user?page={i}"
#     #         payload = payload
#     #         headers = headers
#     #         members = requests.request("GET", url, headers=headers, data=payload).json()['results']
#     #         # print(members)

#     #         if members not in pages:
#     #             pages.append(members)

#     #     pages = ([x for xs in pages for x in xs])
#     #     # print(pages)
        
#     #     for x in pages:
#     #         client_id = x['id']    
#     #         firstname = x['firstname'] 
#     #         surname = x['surname'] 

           
#     #         fullname = f'{firstname} {surname}'
               

#     #         profile_url = x['profilePicture'] 
#     #         contact = x['phone'] 
#     #         email_address = x['email'] 
#     #         level = x['level'] 
#     #         status = x['status'] 
#     #         branch = x['branchId'] 

#     #     if len(Clients.objects.filter(client_id=client_id)) > 0:
#     #         pass  
#     #     else:
#     #         def save(self):
#     #             user = User.save(commit=False)
#     #             user.is_staff = True
#     #             user.save()
#     #             client = Clients.objects.create(member=user)
#     #             client.client_id = client_id
#     #             client.profile_url = profile_url
#     #             client.contact = contact
#     #             client.email_address = email_address
#     #             client.level = level
#     #             client.status = status
#     #             client.branch = branch
#     #             print(user)         

        

