import base64
import configparser
import json
import pandas as pd
import requests

config = configparser.ConfigParser()
config.read("Config.ini")
skype = config['SKYPE']
user = config['USER']


def basic_auth(account):
    data = user["email"] + ":" + account
    encodedBytes = base64.b64encode(data.encode("utf-8"))
    authCode = str(encodedBytes, "utf-8")
    return authCode


def testrun_id_to_file(prev,ga):
    dict = {"Prev%s"%skype["SkypeVersion"]:prev, "ga%s"%skype["SkypeVersion"]:ga}
    with open("Testrun_for_versions.txt", "w") as json_file:
        json.dump(dict, json_file)


def testrun_id_from_file():
    with open("./Files/Testrun_for_versions.txt", "r") as json_file:
        data = json.load(json_file)
        print(data["Prev%s"%skype["SkypeVersion"]])
        print(data["ga%s" % skype["SkypeVersion"]])


def create_testrun(title,ref):
    df = pd.read_excel('./Files/Testcaseslist.xlsm')  # can also index sheet by name or fetch all sheets
    Testcases = df['IDs'].tolist()

    url = "https://smarshcorp.testrail.io/index.php?/api/v2/add_run/20"
    Payload = json.dumps({
        "suite_id": 1492,
        "name": title,
        "assignedto_id": skype["TestRunAssignmentid"],
        "refs": ref,
        "include_all": False,
        "case_ids": Testcases
    })
    authCode = basic_auth(user["TestrailAPIToken"])
    headers = {
        'Authorization': 'Basic ' + authCode,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=Payload, timeout=60)
    print('Output=', response.json())
    jsondata = response.json()
    assert response.status_code == 200
    return jsondata['id']
