""""
This node take the information about Emotion and Attention provided by the Morphcast SDK
and publish it to make it available to the Impression Detection Node.
"""
import time
import requests
import json

url='http://127.0.0.1:8001/' #morphcast Flask server 
headers= {'Content-Type':'application/json'}

data = {
}

url2 = 'http://127.0.0.1:4000' # Impression Detection Flask server

def publish_perception():
    resp=requests.put(url+'get_input', json=data, headers=headers)
    new_perception=eval(resp.text)["new_perception"]  
    print(new_perception)
    #new_perception ="True"
    time.sleep(3)
    if new_perception=="True":
        perc=eval(resp.text)["perception"]
        print(perc)
        #perc = input("morphcast string: ") #per test senza morphcast decomentare
        #conver to json 
        data2 = json.dumps(perc)
        #post on Impression Node
        requests.post(url2+"/morphcast_perception", json=data2)
        
print("Emotion Attention Perception Node")

while(1):
    time.sleep(3)
    publish_perception()