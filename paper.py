import requests
import json

folder = "docs/"
api_file = open("api.txt", 'r')
api = api_file.read()
if api[-1] == '\n':
    api = api[:-1]
api_file.close()


# gets the request and writes it to file
def fetch_document(document_id):
    url = "https://api.dropboxapi.com/2/paper/docs/download"    
    headers = {
        "Authorization": "Bearer " + api,
        "Dropbox-API-Arg": '{"doc_id":"' + document_id + '","export_format":{".tag":"markdown"}}'
    }
    r = requests.post(url, headers=headers)
    if (r.status_code == 200):
        j = json.loads(r.headers["Dropbox-Api-Result"])
        filename = j["title"]
        FILE = open(folder + filename, 'w')
        FILE.write(document_id + '\n')
        FILE.write(r.headers["Dropbox-Api-Result"] + '\n')
        FILE.write(r.text)
        FILE.close()
        print("fetched!")
    else:
        print("request failed!")
    return r

def push_document(filename):
    url = "https://api.dropboxapi.com/2/paper/docs/update"    
    FILE = open(folder + filename, 'r')
    document_id = FILE.readline()[:-1]
    j = FILE.readline()[:-1]
    j = json.loads(j)
    data = FILE.read()
    FILE.close()    
    headers = {
        "Authorization": "Bearer " + api,
        "Content-Type": "application/octet-stream",
        "Dropbox-API-Arg": '{"doc_id":"' + document_id + '","doc_update_policy":{".tag":"overwrite_all"},"revision":' + str(j["revision"]) + ',"import_format":{".tag":"markdown"}}'
    }    
    r = requests.post(url, headers=headers, data=data)
    if (r.status_code == 200):
        print("paper doc updated!")
    else:
        print("paper doc failed to update")
    return r
    
    
    
r = fetch_document("kFER21Yoht9CZoMabbZIF")
print("Change the document")
input()
r = push_document("emacs test doc")

# url = "https://api.dropboxapi.com/2/paper/docs/update"
# filename = "emacs test doc"

# FILE = open(folder + filename, 'rb')
# document_id = (FILE.readline()[:-1]).decode("utf-8")
# j = (FILE.readline()[:-1]).decode("utf-8")
# j = json.loads(j)
# data = FILE.read()
# FILE.close()    
# headers = {
#     "Authorization": "Bearer " + api,
#     "Content-Type": "application/octet-stream",
#     "Dropbox-API-Arg": '{"doc_id":"' + document_id + '","doc_update_policy":{".tag":"append"},"revision":' + str(j["revision"]) + ',"import_format":{".tag":"markdown"}}'
# }    
# r = requests.post(url, headers=headers, data=data)
# if (r.status_code == 200):
#     print("paper doc updated!")
# else:
#     print("paper doc failed to update")

