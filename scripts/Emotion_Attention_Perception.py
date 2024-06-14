""""
This node take the information about Emotion and Attention provided by the Morphcast SDK
and publish it to make it available to the Impression Detection Node.
"""
import time
import requests
import json
from datetime import datetime

url='http://127.0.0.1:8001/' #morphcast Flask server 
headers= {'Content-Type':'application/json'}

data = {
}

url2 = 'http://127.0.0.1:4000' # Impression Detection Flask server
old_values = "0_N"
count = 0
file_emotion="../test/morphcast_data.txt"
file = open(file_emotion, 'a')
file.write("Begin "+str(datetime.now())+"\n")
file.flush()
def send_morphcast(perc):
    print(str(time.time())+" : "+str(perc))
    #perc = input("morphcast string: ") #per test senza morphcast decomentare
    #conver to json 
    data2 = json.dumps(perc)
    #post on Impression Node
    requests.post(url2+"/morphcast_perception", json=data2) 
       

def publish_perception():
    global old_values, count
    resp=requests.put(url+'get_input', json=data, headers=headers)
    new_perception=eval(resp.text)["new_perception"]  
    print(new_perception)
    #new_perception ="True"
    time.sleep(3)
    if new_perception=="True":
        perc=eval(resp.text)["perception"]
        file.write(str(datetime.now())+" : "+str(perc)+"\n")
        if(perc == old_values and count <2):
            count += 1
            send_morphcast(perc)
        elif(perc != old_values):
            old_values = perc
            count = 0
            send_morphcast(perc)
        else: 
            print("Not sending new perception since has been send already 2 times")
        file.flush()
        
print("Emotion Attention Perception Node")

while(1):
    time.sleep(3)
    publish_perception()