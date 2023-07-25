# import json
# import requests
# import os
# from login.models import ClientDetails
# import environ

# env = environ.Env()
# environ.Env.read_env()

# base_url = "https://db-api-v2.akwaabasoftware.com"

# login_headers = {
#   'Content-Type': 'application/json',
#   'Cookie': 'csrftoken=cMrEAoqAfPVtpPCRsc5EW8MNg7GuNMukbCI1VKL8MjTaxV5VsM5lboltWF0Pv9sp; sessionid=oqefvhuzbfzgbhxev9ih3g2mca6p9x10'
# }


# try:
#     detail = ClientDetails.objects.all().last()
#     payload = json.dumps({ "token": detail.token })
#     url = base_url + "/clients/verify-token"

#     payload = payload
#     headers = login_headers
#     token = requests.request("POST", url, headers=login_headers, data=payload).json()['token']
#     user = requests.request("POST", url, headers=login_headers, data=payload).json()['user']

# except:
#     payload = json.dumps({ "phone_email": env('LOGIN_EMAIL'), "password": env('LOGIN_PASSWORD'), "checkDeviceInfo": False })

#     url = base_url +"/clients/login"

#     payload = payload
#     headers = login_headers
#     token = requests.request("POST", url, headers=login_headers, data=payload).json()['token']
#     user = requests.request("POST", url, headers=login_headers, data=payload).json()['user']


# # login request
# # url = "https://db-api-v2.akwaabasoftware.com/clients/login"
# # url = "https://db-api-v2.akwaabasoftware.com/clients/verify-token"

# # payload = payload
# # headers = login_headers
# # token = requests.request("POST", url, headers=login_headers, data=payload).json()['token']
# # user = requests.request("POST", url, headers=login_headers, data=payload).json()['user']




# client_id = user['id']
# new_id = user['id']
# client_firstname = user['firstname']
# client_surname = user['surname']
# accountHolder = f"{client_firstname} {client_surname}" 
# client_branch = user['branchId']
# account_id = user['accountId']
# branch_id = user['branchId']

# # print(account_id)
# # print(client_id)


# members_headers = {
#   'Authorization': f'Token {token}',
#   'Content-Type': 'application/json',
#   'Cookie': 'csrftoken=Ly8oYWb8c70C2CDUYfFd0poVjCL91Octs99w3q6rGjSu8L2SaPVDoGPvJ4tKQIda; sessionid=4zyr1pvz9r6hyu8sqvuh0gqqxsymo56n'
# }


# members_url = base_url + "/members/user?datatable_plugin&length=100"

# members_payload = json.dumps({})

# # client_members = requests.request("GET", members_url, headers=members_headers, data=members_payload).json()['data']




# # url = "https://openexchangerates.org/api/currencies.json?prettyprint=false&show_alternative=false&show_inactive=false&app_id=usd"

# # headers = {"accept": "application/json"}

# # monies = requests.get(url, headers=headers).json()


# # Generate sms token
# # sms_url = "https://app.nstacom.com/api/compose/generate_token"
# # sms_payload = {'phone_number': '0206007255','password': '112233'}
# # headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
# # msg = requests.request("POST", sms_url, headers=headers, json=sms_payload).json()['msg']
# # manilla_token = "120648ed2401ff3fab8f1f5a58c49eb0f58defce5afadb3752a6b3ac0983928e"
# # print(response)

