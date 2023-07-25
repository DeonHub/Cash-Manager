# import requests
# import json


# login_url = "https://db-api-v2.akwaabasoftware.com/clients/login"

# login_payload = json.dumps({ "phone_email": "clickcomgh@gmail.com", "password": "password2" })

# headers = {
#   'Content-Type': 'application/json',
#   'Cookie': 'csrftoken=rmhj1YLmx6cooyU3xzuHWU58c03XYV3KKXwGsIXtRxu0HXhYIELv9coTbLNftFQF; sessionid=bf69ey4165pxvx0ljrpwuwziielbccbn'
# }

# tokenize = requests.request("POST", login_url, headers=headers, data=login_payload).json()['token']

# print()


# members_url = "https://db-api-v2.akwaabasoftware.com/clients/account?length=100&datatable_plugin"

# payload = json.dumps({})

# headers = {
#   'Authorization': f'Token {tokenize}',
#   'Content-Type': 'application/json',
#   'Cookie': 'csrftoken=rmhj1YLmx6cooyU3xzuHWU58c03XYV3KKXwGsIXtRxu0HXhYIELv9coTbLNftFQF; sessionid=bf69ey4165pxvx0ljrpwuwziielbccbn'
# }

# members = requests.request("GET", members_url, headers=headers, data=payload).json()['data']
# print(members)


# for member in members:

#     hash_url = "https://db-api-v2.akwaabasoftware.com/clients/hash-hash"

#     payload = json.dumps({ "accountId": member['id'] })

#     headers = {

#     'Content-Type': 'application/json',
#     'Cookie': 'csrftoken=qKb26BppnLj2fEJzoV2orUrUxCUPYZoLAFNoEiqvqTRp5pfi1Oy114lUvotVB8vS; sessionid=b028i09gi510b2jkoekesyzf0nkwie3m'
#     }

#     token = requests.request("POST", hash_url, headers=headers, data=payload).json()['token']



#     info_url = "https://db-api-v2.akwaabasoftware.com/clients/subscription/info?ordering=-id"

#     payload = json.dumps({ })

#     headers = {
#     'Authorization': f'Token {token}',
#     'Content-Type': 'application/json',
#     'Cookie': 'csrftoken=qKb26BppnLj2fEJzoV2orUrUxCUPYZoLAFNoEiqvqTRp5pfi1Oy114lUvotVB8vS; sessionid=b028i09gi510b2jkoekesyzf0nkwie3m'
#     }

#     results = requests.request("GET", info_url, headers=headers, data=payload).json()['results']

#     for data in results:
#         for x in data['clientInfo']:
#             print(x['subscriptionInfo'])
#         print(data['membershipSize'])
#         print()
#         print()


    


