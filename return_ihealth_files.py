import requests
import json
import xmltodict
import os
import re
import csv
import tempfile
import jmespath
import jinja2
from user_info import bauth

##################
##   Variables  ##
##################
qkid = 00000000
## file name returned from ihealth
fname = "/stat_module.xml"
## strip just file name
nfname = re.split("\\/|\\.", fname)
## renamed file in json extension stat_module.json
fname_json = nfname[1] + ".json"


def auth_in():
    global session, rtoken
    url = "https://identity.account.f5.com/oauth2/ausp95ykc80HOU7SQ357/v1/token"
    headers = {"accept": "application/json", "authorization": "Basic " + bauth}
    payload = {"grant_type": "client_credentials", "scope": "ihealth"}
    session = requests.session()
    r_token = session.post(url, headers=headers, data=payload)
    r = r_token.content
    r_json = json.loads(r)
    rtoken = r_json.get("access_token")
    print("Auth Token ", r_token.status_code)

# List all file names based on qkview id number
def list_files(id):
    global session, rtoken
    url = (
        "https://ihealth2-api.f5.com/qkview-analyzer/api/qkviews/" + str(id) + "/files"
    )
    headers = {
        "Accept": "application/vnd.f5.ihealth.api.v1.0+json",
        "User-Agent": "F5SE",
        "Authorization": "Bearer " + rtoken,
    }
    session = requests.session()
    r_token = session.get(url, headers=headers)
    r = json.loads(r_token.content)
    return r

# get just the file id from file name
def search(name, f_l):
    # return [element for element in f_l if element["value"] == name]
    g = [element.get("id") for element in f_l if element["value"] == name]
    # g = g.get('id')
    return g.pop()


# get file contents (xml) and write to temp file
def get_files(id, fid):
    global session, rtoken
    url = (
        "https://ihealth2-api.f5.com/qkview-analyzer/api/qkviews/"
        + str(id)
        + "/files/"
        + str(fid)
    )
    headers = {
        "Accept": "application/vnd.f5.ihealth.api.v1.0+json",
        "User-Agent": "F5SE",
        "Authorization": "Bearer " + rtoken,
    }
    session = requests.session()
    r_token = session.get(url, headers=headers)
    # r = json.loads(r_token.content)
    return r_token.content

def write_file(name, func):
    with open(name, "w") as f:
        f.write(func)
        f.close()

##connect to iHealth API
auth_in()
##list files connected to qkview
#print(list_files(qkid))

## find stat_module file name in list and return file id
fid = search(fname, list_files(qkid))
## create temporary file with contents of stat_module.xml
print("create temp")
temp_xml = tempfile.NamedTemporaryFile(mode="w+b", dir="/Users/C.Wise", delete=True)
temp_xml.write(get_files(qkid, fid))
temp_xml.seek(0)
#
## convert temprary file from xml to json
data_dict = xmltodict.parse(temp_xml.read())
## this will delete the temp xml file
temp_xml.close()
json_data = json.dumps(data_dict, indent=2)
## write file stat_module.json
with open(fname_json, "w") as jf:
    jf.write(json_data)
    jf.close()
