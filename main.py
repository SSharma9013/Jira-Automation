import base64
import configparser
from datetime import date
from Jira import create_parent_ticket, create_subtask_ticket
from Testrail import create_testrun, testrun_id_to_file

today = date.today()

config = configparser.ConfigParser()
config.read("Config.ini")
skype = config['SKYPE']
user = config['USER']


def basic_auth(account):
    data = user["email"] + ":" + account
    encodedBytes = base64.b64encode(data.encode("utf-8"))
    authCode = str(encodedBytes, "utf-8")
    return authCode



# Creates a main ticket for the recently release Skype version which we have to mention in the config file
parent = create_parent_ticket()


# create a subtask Preview Compatibility Test
with open('./Files/Preview_Compatibility_Test_desc.txt', 'r+') as f:
    # read file
    file_source = f.read()
    # replace 'Skype_version' with 'relevent version' in the file
    temp_desc = file_source.replace('version', skype["SkypeVersion"])
    date = today.strftime("%B %d, %Y")
    temp_desc = temp_desc.replace('Date', date)
summary = skype["SkypeVersion"] + " Preview Compatibility Test"
Preview_ref = create_subtask_ticket(parent, summary, temp_desc,"Test Sub-Task", "Priority 2 - High", skype["Suraksha"])
id_prev = create_testrun(summary,Preview_ref)


# create a subtask GA Compatibility Test
with open('./Files/GA_Compatibility_Test_desc.txt', 'r+') as f:
    # read file
    file_source = f.read()
    # replace 'Skype_version' with 'relevent version' in the file
    temp_desc = file_source.replace('version', skype["SkypeVersion"])
summary = skype["SkypeVersion"] + " GA Compatibility Test"
GA_ref = create_subtask_ticket(parent, summary, temp_desc,"Test Sub-Task", "Priority 1 - Highest", skype["Suraksha"])
id_ga = create_testrun(summary,GA_ref)

testrun_id_to_file(id_prev,id_ga)

# create a subtask Approve Skype version in Staging 2
with open('./Files/Approve_In_Staging.txt', 'r+') as f:
    # read file
    file_source = f.read()
    # replace 'Skype_version' with 'relevent version' in the file
    temp_desc = file_source.replace('version', skype["SkypeVersion"])
summary = "Approve Skype " + skype["SkypeVersion"] + " in Staging 2"
create_subtask_ticket(parent, summary, temp_desc,"DB sub-task", "Priority 3 - Medium", skype["Suraksha"])

# create a subtask Update Support Chart
with open('./Files/Update_doc.txt', 'r+') as f:
    # read file
    file_source = f.read()
    # replace 'Skype_version' with 'relevent version' in the file
    temp_desc = file_source.replace('version', skype["SkypeVersion"])
summary = "IMPM: Update Support Chart"
create_subtask_ticket(parent, summary, temp_desc,"Release Sub-Task", "Priority 3 - Medium", skype["Suraksha"])


# create a subtask to Skype Skype version to Production
temp_desc = "Add %s to approved client list in production." % skype["SkypeVersion"]
summary = "Approve Skype %s in production" % skype["SkypeVersion"]
create_subtask_ticket(parent, summary, temp_desc,"DB sub-task", "Priority 2 - High", skype["Niraj"])
