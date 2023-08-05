import requests
import json

class requestMode(object):
    post = "post"
    get = "get"
    put = "put"
    delete = "delete"    
        
def sendRequest(url, header, params = "", content = "", 
                rMode = requestMode.post):
     
    if rMode == "post":
        rMode = requests.post
    elif rMode == "get":
        rMode = requests.get
    elif rMode == "put":
        rMode = requests.put
    elif rMode == "delete":
        rMode = requests.delete     
    
    status = True
    try:
        response = rMode(
            url=url,
            headers=header,
            params=params,
            data=json.dumps(content)
        )
        if response.status_code < 300 and response.status_code >= 200:
            status = True
        else:
            status = False
        content = response.content
    
    except requests.exceptions.RequestException:
        status = False
        content = '%s Request failed'%url
    
    return(status, content)