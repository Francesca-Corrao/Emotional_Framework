import time
import requests
url='http://127.0.0.1:8001/'
headers= {'Content-Type':'application/json'}

data = {
}

def publish_perception():
    resp=requests.put(url+'get_input', json=data, headers=headers)
    new_perception=eval(resp.text)["new_perception"]  
    print(new_perception)
    time.sleep(3)
    if new_perception=="True":
        perc=eval(resp.text)["perception"]
        print(perc)

while(1):
    time.sleep(1)
    publish_perception()