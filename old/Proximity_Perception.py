"""
This node use naoqi SDK to connect to Pepper robot and get the information about proximity of the humans.
In particular is uses ALPeoplePerception, ALEngagementZones and ALMemory. 
ALEngagementZones is used to describe and update in an initial state the thre different zones recognized by Pepper:
near-front, far and lateral, very far away and later.
Then form ALMemory it is retrived the list of people id present in the different zones, stored by ALEngagementZones.
This id later used by ALMemory to get the distance of that people from teh robot, stored by ALPeoplePerception. 
"""

from naoqi import ALProxy
import time
import requests
import json
#localhost:51260
#pepper.local.:9559
IP_ADD = "10.0.0.2" #set correct IP 
PORT = 9559 #set correct PORT 

url2 = 'http://127.0.0.1:4000' #impression_detection
class ProximityPerception():
    def __init__(self):
        #set up to connect to Pepper
        self.memory = ALProxy("ALMemory", IP_ADD, PORT) #aggiungere IP e porta
        self.people_perception = ALProxy("ALPeoplePerception", IP_ADD,PORT) #aggiungere IP e porta
        self.engagment_zone = ALProxy("ALEngagementZones",IP_ADD,PORT) #aggiungere IP e porta 
        self.engagment_zone.setFirstLimitDistance(1) 
        self.engagment_zone.setSecondLimitDistance(2)
        self.engagment_zone.setLimitAngle(90)
        self.people = False
        self.people_id = []

    def start(self):
        print("Proximity Perceptioon Started...")
        while(True):
            self.people_id = [] #list of people in the Engagement Zones
            people_list = self.memory.getData("EngagementZones/PeopleInZone1") #look for people in the 1st EZ

            if len(people_list) >0:
                self.people = True
                for p in people_list:
                    print(p)
                    s = "PeoplePerception/Person/"+ str(p) + "/Distance"
                    self.people_id.append(s) 
            else:
                #if there are no people in Zone 1 look for people in zone 2
                people_list = self.memory.getData("EngagementZones/PeopleInZone2")
                if len(people_list) >0:
                    self.people = True
                    for p in people_list:
                        print(p)
                        s = "PeoplePerception/Person/"+ str(p) + "/Distance"
                        self.people_id.append(s)
            
            self.people = True
            if(self.people):
                dist = 0 
                for p in self.people_id:
                    dist = self.memory.getData(p)
                    print(p, " : ", dist)
                #dist = float(input("proximity: ")) #per test senza Pepper decommentare
                #post on Impression Node API
                data2 = json.dumps(dist)
                #requests.post(url2+"/proximity_perception", json=data2)

            else:
                print("no People detected")
                #send maximum distance from robot ? or don't post nothing ? 
            time.sleep(3)
        pass


#print("Hello world!")
PP_module = ProximityPerception()
PP_module.start()



