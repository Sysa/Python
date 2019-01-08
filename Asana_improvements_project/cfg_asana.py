#!/usr/bin/env python
class asana_connect:
    api_token = "0/YourKey"

asana_shift = {
    "EU":["47267243578246", "46031119571733", "135417377517630", "47267243578271", "659139643623752", "388947645163060"],
    "US":["46031119571733", "47267243578234", "47174861801278", "47250514209966", "46031104126842", "47176204518437" ],
    "APAC":["47267243578257", "46031119571733", "47174861801278", "388947645163060"]
    }
#list of asana's users:

#to get all users, run the following section of code:
### USERS ###
# import asana
# client = asana.Client.access_token(asana_connect.api_token)
# users = client.users.find_by_workspace('712734135166')
# for user in users:
#     print (user)

### USERS ###

# 47267243578246 - alexh
# 46031119571733 - SergeySi
# 47267243578257 - ScottH
# 47267243578234 - EricR
# 62960631772676 - GWOps bot
# 47174861801278 - JeffG
# 47250514209966 - MatthewN
# 46031104126842 - NikitaT
# 47176204518437 - SmaK
# 135417377517630 - Kiselev
# 47267243578271 - Ana
# 388947645163060 - chunyee
# 659139643623752 - Moskin





# print (asana_shift.eu)
# for item in asana_shift.eu:
#     print(item)

# class siebel_info:
#     dsn = "SiebelFreeTDS"
#     uid = "ALEXH"
#     pwd = "ALEXH"

# class asana_info:
#     token = "0/YourKey"
#     project_ids = {"486028012641664", "47279160937347"}
# #
# siebel_info2 = {'dsn': 'SiebelFreeTDS',
#          'uid' : 'ALEXH',
#          'pwd' : 'ALEXH'}

# 47279160937347 - problems in GW
# 486028012641664 - Asana API test