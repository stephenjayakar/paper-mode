import requests
import json

api_file = open("api.txt", 'r')
api = api_file.read()
api_file.close()

url = "https://api.dropboxapi.com/2/paper/docs/download"

# gets the request and writes it to file
def fetch_document(document_id):
    headers = {
        "Authorization": "Bearer " + api,
        "Dropbox-API-Arg": '{"doc_id":"' + document_id + '","export_format":{".tag":"markdown"}}'
    }
    r = requests.post(url, headers=headers)
    if (r.status_code == 200):
        j = json.loads(r.headers["Dropbox-Api-Result"])
        filename = j["title"]
        FILE = open(filename, 'w')
        FILE.write(document_id + '\n')
        FILE.write(r.headers["Dropbox-Api-Result"] + '\n')
        FILE.write(r.text)
        FILE.close()
        print("fetched!")
    else:
        print("request failed!")
    return r

def push_document(filename):
    FILE = open(filename, 'r')
    document_id = FILE.readline()[:-1]
    j = FILE.readline()[:-1]
    j = json.loads(j)
    data = FILE.read()
    FILE.close()    
    headers = {
        "Authorization": "Bearer " + api,
        "Content-Type": "application/octet-stream",
        "Dropbox-API-Arg": '{"doc_id":"' + document_id + '","doc_update_policy":{".tag":"append"},"revision":' + str(j["revision"]) + ',"import_format":{".tag":"markdown"}}'
    }    
    r = requests.post(url, headers=headers, data=data)
    if (r.status_code == 200):
        print("paper doc updated!")
    else:
        print("paper doc failed to update")
    return headers, r
    
    
    
r = fetch_document("kFER21Yoht9CZoMabbZIF")
print("Change the document")
input()

filename = "emacs test doc"

FILE = open(filename, 'r')
document_id = FILE.readline()[:-1]
j = FILE.readline()[:-1]
j = json.loads(j)
data = FILE.read()
FILE.close()    
headers = {
    "Authorization": "Bearer " + api,
    "Content-Type": "application/octet-stream",
    "Dropbox-API-Arg": '{"doc_id":"' + document_id + '","doc_update_policy":{".tag":"append"},"revision":' + str(j["revision"]) + ',"import_format":{".tag":"markdown"}}'
}    
r = requests.post(url, headers=headers, data=data)
if (r.status_code == 200):
    print("paper doc updated!")
else:
    print("paper doc failed to update")

