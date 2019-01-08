import asana

import datetime
import time

script_start_time = datetime.datetime.now()

#date = datetime.datetime.now().isoformat()
date = datetime.datetime.utcnow()
#datetime.datetime.now()
print(date)
time_delta = datetime.timedelta(days=2)
report_time = date - time_delta
# report_time = date.today()-time_delta
# ISO-8601:

#report_time = report_time.isoformat()
#yyyy-mm-ddThh:mm:ss+zzzz
report_time = report_time.strftime("%Y-%m-%dT%H:%M:%SZ")

#print(date.strftime("%Y%m%dT%H%M%S.%fZ"))

#report_time = datetime.datetime.utcnow().isoformat() + 'Z'
#report_time = datetime.datetimereport_time, "%Y%m%dT%H%M%S.%fZ")
print(report_time)

def sendMeMessage(messageSender,messageDestination,messageBody,messageTitle):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # me == the sender's email address
    # you == the recipient's email address
    #msg = MIMEMultipart(messageBody)
    msg = MIMEText(messageBody, 'html')
    msg['Subject'] = messageTitle
    msg['From'] = messageSender
    msg['To'] = messageDestination
    s = smtplib.SMTP('mail.chicago.YourCompanyName')
    s.send_message(msg)
    s.quit()


client = asana.Client.access_token('0/YourKey')
me = client.users.me()

#table style:
htmlcssStyle="<style> table{border: none; border-collapse: collapse; border-bottom: 1px solid; border-top: 1px solid;" \
         "border-right: 1px solid;" \
         "align:center;" \
         "font: normal 12px/150% Arial, Helvetica, sans-serif;}" \
         "table td{align:center;padding: 3px 3px; border-left: 1px solid #000;}" \
         "thead.modifiedTasks {text-align: center; background-color: rgb(255, 131, 0)}" \
         "thead.completedTasks {text-align: center; background-color: rgb(135, 255, 0)}" \
         "tr:nth-child(even) {background-color: #f2f2f2}" \
         "</style>"

HTMLOutput = htmlcssStyle + "<html><body>"

completedTasksHTMLTable = "<center><h2> Completed tasks since " + report_time[0:19] + " UTC </h2></center><table border=1><thead class=completedTasks><tr><td>" \
                          "Task name</td>" \
                          "<td>Completed since (UTC)</td>" \
                          "<td>Description</td>" \
                          "<td>Last activities</td>" \
                          "</tr></thead>" \
                          "<tbody>"


modifiedTasksHTMLTable = "<center><h2> Modified tasks since " + report_time[0:19] + " UTC </h2></center><table border=1><thead class=modifiedTasks><tr><td>" \
                          "Task name</td>" \
                          "<td>Modified at (UTC)</td>" \
                          "<td>Description</td>" \
                          "<td>Last activities</td>" \
                          "</tr></thead>" \
                          "<tbody>"

def getTaskActivities(taskID,report_time):
    #task id - 234738465508060
    taskActivities = client.tasks.stories(taskID)
    lastComments = ""
    for taskActivity in taskActivities:
        #print(taskActivity)
        if taskActivity['created_at'] > report_time:
            #print(taskActivity['text'])

            lastComments += taskActivity['text'] + " <br> "
    return lastComments

def getCompletedTasks(asanaClient, projectID, report_time):
    tasks_in_project = asanaClient.tasks.find_by_project(projectID, params={
        'opt_fields': 'id,completed,completed_at,name,notes,modified_at', 'completed_since': report_time})
    for task in tasks_in_project:
        if task['completed'] == True:
            #print(task)
            global completedTasksHTMLTable
            link_to_tag = " <a href=\"https://app.asana.com/0/" + str(projectID) + "/" + str(task['id']) + "\"> " + task['name'] + " </a>"
            completedTasksHTMLTable += "<tr><td><a href=" + link_to_tag + "</a></td>" + "<td>"\
                                       + task['completed_at'][:10]\
                                       + " at " + task['completed_at'][12:19]\
                                       + "</td>" + "<td>"\
                                       + task['notes'] + "</td>"\
                                       + "<td>" + getTaskActivities(task['id'],report_time) + "</td>"\
                                       + "</tr>"
            #print(completedTasksHTMLTable)
        else:
            #print(task)
            if task['modified_at'] > report_time:
                #print(task)
                global modifiedTasksHTMLTable
                link_to_tag = " <a href=\"https://app.asana.com/0/" + str(projectID) + "/" + str(task['id']) + "\"> " + \
                              task['name'] + " </a>"
                modifiedTasksHTMLTable += "<tr><td><a href=" + link_to_tag + "</a></td>" + "<td>"\
                                       + task['modified_at'][:10]\
                                       + " at " + task['modified_at'][12:19]\
                                       + "</td>" + "<td>" + task['notes'] + "</td>"\
                                       + "<td>" + getTaskActivities(task['id'],report_time) + "</td>"\
                                       + "</tr>"



projects_in_workspace = client.projects.find_by_workspace(712734135166,params={'opt_fields':'id,name,modified_at,archived','archived': 'False'})
for project in projects_in_workspace:
    #print(project)
    #getCompletedTasks(client,project['id'],report_time)
    #print(project['id'])
    #print(report_time)
    getCompletedTasks(client,project['id'],report_time)
    #we can handle reate limits via 'Retry-After' response header from Asana's side, but...just pause each big request for 0.5 second and keep calm:
    time.sleep(0.2)
####getCompletedTasks(client, 47273643661586, report_time)

# uncompleted tasks
#tasks_in_project = client.tasks.find_by_project(47273643661586, params={'completed_since':'2016-12-25T00:00:00Z'})
# tasks_in_project = client.tasks.find_by_project(47273643661586, params={'completed_since':report_time})
# for task in tasks_in_project:
#     print(task)

# tasks_in_project = client.tasks.find_by_project(47273643661586, params={'opt_fields':'id,completed,completed_at,name,notes','completed_since':report_time})
# for task in tasks_in_project:
#     print(task)
#


print (datetime.datetime.now() - script_start_time)


HTMLOutput += completedTasksHTMLTable + "</tbody></table>" + modifiedTasksHTMLTable + "</tbody></table></body></html>"

#generating HTML doc:
# try:
#     with open("AsanaReport.html", "w", encoding='utf-8') as html_file:
#         html_file.write(HTMLOutput)
# #     #Html_file.close()
# except Exception as E:
#     print(E)


#sending results: (go ahead without try/catch):
#sendMeMessage('alexh@YourCompanyName.com', 'alexh@YourCompanyName.com', HTMLOutput, 'Asana summary report')
sendMeMessage('GWOPS@YourCompanyName.com', 'GWREP@YourCompanyName.com', HTMLOutput, 'Asana Summary Report')

