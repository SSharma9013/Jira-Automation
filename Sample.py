import base64
import configparser
import json
import pandas as pd
import requests
from datetime import date

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


def parent_payload(summary_text,description_text):
    parent_payload = \
        {
            "fields":
                {
                    "project": {"key": "SKY"},
                    "fixVersions": [{"name": "%s" % skype["FixVersion"]}],
                    "summary": "%s" % summary_text,
                    "description": "%s" % description_text,
                    "issuetype": {"name": "Story"},
                    "priority": {"name": "Priority 3 - Medium"},
                    "components": [{"id": "12098"}],
                    "assignee": {"id": "%s" % skype["Suraksha"]}
                }
        }
    return parent_payload


def subtask_payload(parent, summary_text, description_text, issuetype, priority, assignee):
    subtask_payload = \
        {
            "fields":
                {
                    "parent":{"key": "%s" % parent},
                    "project": {"key": "SKY"},
                    "fixVersions": [{"name": "%s" % skype["FixVersion"]}],
                    "summary": "%s" % summary_text,
                    "description": "%s" % description_text,
                    "issuetype": {"name": "%s" % issuetype},
                    "priority": {"name": "%s" % priority},
                    "assignee": {"id": "%s" % assignee }
                }
        }
    return subtask_payload


def create_parent_ticket():
    with open('./Files/ParentTicketDescription.txt', 'r+') as f:
        # read file
        file_source = f.read()
        # replace 'Skype_version' with 'relevent version' in the file
        temp_desc = file_source.replace('version', skype["SkypeVersion"])
    summary = "Skype 8: Compatibility test for Skype " + skype["SkypeVersion"]
    payload = json.dumps(parent_payload(summary, temp_desc))
    url = "https://presensoft.atlassian.net/rest/api/2/issue/"
    authCode = basic_auth(user["JiraAccessToken"])
    headers = {
        'Authorization': 'Basic ' + authCode,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=payload, headers=headers, timeout=60)
    jsondata = response.json()
    print('Output=', jsondata)
    assert response.status_code == 201
    return jsondata['key']


def create_subtask_ticket(parent, summary, temp_desc, issuetype, priority, assignee):
    payload = json.dumps(subtask_payload(parent, summary, temp_desc,issuetype, priority, assignee ))
    url = "https://presensoft.atlassian.net/rest/api/2/issue/"
    authCode = basic_auth(user["JiraAccessToken"])
    headers = {
        'Authorization': 'Basic ' + authCode,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=payload, headers=headers, timeout=60)
    print('Output=', response.json())
    assert response.status_code == 201


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
create_subtask_ticket(parent, summary, temp_desc,"Sub-Task", "Medium", skype["Suraksha"])



# create a subtask GA Compatibility Test
with open('./Files/GA_Compatibility_Test_desc.txt', 'r+') as f:
    # read file
    file_source = f.read()
    # replace 'Skype_version' with 'relevent version' in the file
    temp_desc = file_source.replace('version', skype["SkypeVersion"])
summary = skype["SkypeVersion"] + " GA Compatibility Test"
create_subtask_ticket(parent, summary, temp_desc,"Sub-Task", "Medium", skype["Suraksha"])


# create a subtask Approve Skype version in Staging 2
with open('./Files/Approve_In_Staging.txt', 'r+') as f:
    # read file
    file_source = f.read()
    # replace 'Skype_version' with 'relevent version' in the file
    temp_desc = file_source.replace('version', skype["SkypeVersion"])
summary = "Approve Skype " + skype["SkypeVersion"] + " in Staging 2"
create_subtask_ticket(parent, summary, temp_desc,"Sub-task", "Medium", skype["Suraksha"])

# create a subtask Update Support Chart
with open('./Files/Update_doc.txt', 'r+') as f:
    # read file
    file_source = f.read()
    # replace 'Skype_version' with 'relevent version' in the file
    temp_desc = file_source.replace('version', skype["SkypeVersion"])
summary = "IMPM: Update Support Chart"
create_subtask_ticket(parent, summary, temp_desc,"Sub-Task", "Medium", skype["Suraksha"])


# create a subtask to Skype Skype version to Production
temp_desc = "Add %s to approved client list in production." % skype["SkypeVersion"]
summary = "Approve Skype %s in production" % skype["SkypeVersion"]
create_subtask_ticket(parent, summary, temp_desc,"Sub-task", "Medium", skype["suraksha"])
