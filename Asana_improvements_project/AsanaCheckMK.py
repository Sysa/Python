import asana
import re
import requests
import time
from asana.error import InvalidTokenError 

client = asana.Client.access_token('0/7e94615fda30ca7333618b5fcf8acdae')
me = client.users.me()
checkmk_user='scotthBot'
secret='IOHYHPAW@ARSNLSIGLID'
projectID=594431268083354


##Get all users in GWOps team
teamid=46031119571717
gwops_users=client.teams.users(teamid,params={'opt_fields': 'id'})
gwops_users=list(gwops_users)
 
#get initial sync token
sync=''

while True:
	try:
		events=client.events.get_by_project(projectID,params={'sync':sync})

	except InvalidTokenError as e: 
		sync=e.sync
	       	events=client.events.get_by_project(projectID,params={'sync':sync})
	

	sync=events['sync']
	events=events['data']
	if events: print(events)
	print(sync)
	time.sleep(20)

if events!='':
	for event in events:
        	if event.get('type')=='task' and event.get('action')=='added':
        	        taskid=(event.get('resource')['id'])
		        #client.tasks.add_followers(taskid, params={'followers': gwops_users})		##uncomment when ready for deployment


def getNewTaskAndAck(asanaClient, projectID, followers):
	tasks_in_project = asanaClient.tasks.find_by_project(projectID, params={
		'opt_fields': 'id,completed,name,notes,followers','completed_since':'now'})  ##Need to change to completed=false,notes,id,follower
	for task in tasks_in_project:
		#print(task['followers'])
		#print(followers)
   		
	     	#asanaClient.tasks.add_followers(task['id'], params={'followers': followers})

		##Retrieves acknowledgement link and 
		try:
			ack_link=re.search('ToAcknowledgeLink:\s(.*?)\s',task['notes']).group(1)
			full_ack_link=(ack_link+'&_username='+checkmk_user+'&_secret='+secret)
			print(full_ack_link)
		except AttributeError:
			ack_link=''
		
		if ack_link != '':
			print(task['name'])
			#ack = requests.get(full_ack_link) ##acknowledges service in checkmk


#add all followers to CheckMk Alarms
getNewTaskAndAck(client,projectID, gwops_users)

# 594431268083354 - CheckMK Alarms
