from naoqi import ALProxy
import time
import requests
import json

#Pepper info to connect
IP_ADD = "10.0.0.2" #set correct IP 
PORT = 9559 #set correct PORT

MAX_DIST = 15 
url2 = 'http://127.0.0.1:4000' #impression_detection
class ProximityPerception():
    def __init__(self):
        #set up to connect to Pepper
        self.memory = ALProxy("ALMemory", IP_ADD, PORT) #aggiungere IP e porta
        self.engagment_zone = ALProxy("ALEngagementZones",IP_ADD,PORT) #aggiungere IP e porta 
        self.engagment_zone.setFirstLimitDistance(1) 
        self.engagment_zone.setSecondLimitDistance(2)
        self.engagment_zone.setLimitAngle(90)
        self.people_id = 0

    def get_people_id(self):
        p = self.people_id
        zone = 1
        while(self.people_id != p and zone<= 3):
            str = "EngagementZones/PeopleInZone"+str(zone)
            people_list = self.memory.getData(str)
            if( len(people_list)==1):
                print("new people(id) found")
                self.people_id= people_list[0]
            elif( len(people_list)>1):
                print("More than one People in Zone"+str(zone)+ "taking the first"):
                self.people_id= people_list[0]
            else:
                zone += 1

    def onInput_onStart(self):
        print("Proximity Perceptioon Started...")
        dist = MAX_DIST
        self.get_people_id()
        while(1):
            people_list = self.memory.getData("EngagementZones/PeopleInZone1")
            people_list.append(self.memory.getData("EngagementZones/PeopleInZone2"))
            people_list.append(self.memory.getData("EngagementZones/PeopleInZone3"))
            if(self.people_id in people_list):
                print("people(id) still visible")
                str = "PeoplePerception/Person/"+ str(self.people_id) + "/Distance"
                dist = self.memory.getData(str)
            else:
                print("People(id) not visible looking for new id")
                self.get_people_id()
            #send distance to Impression Interface
            data2 = json.dumps(dist)
            requests.post(url2+"/proximity_perception", json=data2)
            time.sleep(3) #choose appropriate rate

PP_module = ProximityPerception()
PP_module.onInput_onStart()
    