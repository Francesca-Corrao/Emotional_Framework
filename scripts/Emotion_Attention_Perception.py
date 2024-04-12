import time
import requests
import json
url='http://127.0.0.1:8001/' #morphcast
headers= {'Content-Type':'application/json'}

data = {
}

url2 = 'http://127.0.0.1:4000' #impression_detection
def publish_perception():
    #global data
    #resp=requests.put(url+'get_input', json=data, headers=headers)
    #new_perception=eval(resp.text)["new_perception"]  
    #print(new_perception)
    new_perception ="True"
    time.sleep(3)
    if new_perception=="True":
        #perc=eval(resp.text)["perception"]
        #print(perc)
        #conver to json 
        #post on Impression Node
        i = input("morphcast string: ")
        data2 = json.dumps(i)
        requests.post(url2+"/morphcast_perception", json=data2)

while(1):
    time.sleep(1)
    publish_perception()