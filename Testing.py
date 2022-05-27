import base64
import configparser
import json
from datetime import date
import pandas as pd
import requests
from xlrd import sheet

today = date.today()

config = configparser.ConfigParser()
config.read("Config.ini")
skype = config['SKYPE']
user = config['USER']

def basic_auth():
    data = user["email"] + ":" + user["TestrailAPIToken"]
    encodedBytes = base64.b64encode(data.encode("utf-8"))
    authCode = str(encodedBytes, "utf-8")
    return authCode

def get_run():
    url1 ="https://smarshcorp.testrail.io/index.php?/api/v2/get_run/14339"
    authCode = basic_auth()
    headers = {
        'Authorization': 'Basic ' + authCode,
        'Content-Type': 'application/json'
    }
    response = requests.get(url1, headers=headers, timeout=60)
    print('Output=', response.json())
    assert response.status_code == 200


def prepare_testcases():
    df = pd.read_excel('./Files/Testcaseslist.xlsm')  # can also index sheet by name or fetch all sheets
    Testcases = df['IDs'].tolist()
    List = []
    for i in Testcases:
        List.append({"case_id": i,"status_id": 1 })
    return List


def update_testrun():
    url2 ="https://smarshcorp.testrail.io/index.php?/api/v2/add_results_for_cases/15091"
    authCode = basic_auth()
    headers = {
        'Authorization': 'Basic ' + authCode,
        'Content-Type': 'application/json'
    }
    payload = json.dumps({"results": prepare_testcases()})
    response = requests.post(url2, headers=headers, data=payload, timeout=60)
    print('Output=', response.json())
    assert response.status_code == 200


def testrun_id_to_file():
    a = 1
    b = 2
    dict = {"Prev%s"%skype["SkypeVersion"]:a, "ga%s"%skype["SkypeVersion"]:b}
    with open("./Files/Testrun_for_versions.txt", "w") as json_file:
        json.dump(dict, json_file)

def testrun_id_from_file():
    with open("./Files/Testrun_for_versions.txt", "r") as json_file:
        data = json.load(json_file)
        print(data["Prev%s"%skype["SkypeVersion"]])
        print(data["ga%s" % skype["SkypeVersion"]])


def Wriring_messages_to_file():
    a = "Suraksha"
    b = "Sanjeev"
    c = "Hello"
    dict = {"Sender": a, "Recipient": b, "message": c}
    with open("./Files/Message %s.txt" % today.strftime("%B %d, %Y"), "w") as json_file:
        json.dump(dict, json_file)


def add_test_results():
    df = pd.read_excel('./Files/Testcaseslist.xlsm')  # can also index sheet by name or fetch all sheets
    Testcases = df['IDs'].tolist()
    print(Testcases)

    url = "https://smarshcorp.testrail.io/index.php?/api/v2/add_run/20"
    Payload = json.dumps({
        "suite_id": 1492,
        "name": "8.73 GA Compatibility Test",
        "assignedto_id": 151,
        "refs": "PRES-3066",
        "include_all": False,
        "case_ids": Testcases
    })
    authCode = basic_auth()
    headers = {
        'Authorization': 'Basic ' + authCode,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=Payload, timeout=60)
    jsondata = response.json()
    f = open("./Files/%s.txt" % skype["SkypeVersion"], jsondata['id'])
    f.write("\n")
    print('Output=', response.json())
    assert response.status_code == 200

