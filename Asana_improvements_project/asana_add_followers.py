import asana

import datetime
import time

client = asana.Client.access_token('0/YourKey')
me = client.users.me()

print(me)


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
# 659139643623752 Moskin


gwops_users_array=['62960631772676', '47267243578246', '46031119571733', '47267243578257', '47267243578234', '47174861801278', '47250514209966', '46031104126842', '47176204518437', '135417377517630', '47267243578271', '388947645163060', '659139643623752']

def getCompletedTasks(asanaClient, projectID, followers):
    tasks_in_project = asanaClient.tasks.find_by_project(projectID, params={
            'opt_fields': 'id,completed,completed_at,name,notes,modified_at', 'completed_since': 'now'})
    for task in tasks_in_project:
        print(followers)
        print(task['id'])
        #asanaClient.tasks.add_followers(task['id'], params={'followers': '62960631772676'})
        asanaClient.tasks.add_followers(task['id'], params={'followers': followers})
        print(task)


getCompletedTasks(client,'47279160937347', gwops_users_array)
#add SergeySi to Events in GW Project:
getCompletedTasks(client,'47275593079359', '46031119571733')
getCompletedTasks(client,'47174860852068', '46031119571733')

# 47279160937347 - ongoing issues
# 278929633489128 - symantec AV
# 47275593079359 - Events in GW
# 47174860852068 - vacations and days off