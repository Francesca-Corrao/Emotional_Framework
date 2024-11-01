"""
Pepper's perception module to get
- proximity from user
- gaze level of the user 
and send it to the Impression Detection Node
"""
from naoqi import ALProxy
import time
import requests
import json
from datetime import datetime

#Pepper info to connect
#IP_ADD = "192.168.248.132" #set IP 
IP_ADD= "130.251.13.122" #NAO lab
PORT = 9559 #set PORT

MAX_DIST = 1.5 
url2 = 'http://127.0.0.1:4000' #impression_detection
output_data = {}

file_emotion = "../test/pepper_perception.txt"
file = open(file_emotion, "a")
file.write("Beging" + str(datetime.now()) + "\n")
class ProximityPerception():
    def __init__(self):
        #set up to connect to Pepper
        self.memory = ALProxy("ALMemory", IP_ADD, PORT)
        self.engagment_zone = ALProxy("ALEngagementZones",IP_ADD,PORT)
        self.people_perception = ALProxy("ALPeoplePerception", IP_ADD,PORT)
        self.gaze_analysis = ALProxy("ALGazeAnalysis", IP_ADD,PORT)
        self.engagment_zone.setFirstLimitDistance(1) 
        self.engagment_zone.setSecondLimitDistance(2)
        self.engagment_zone.setLimitAngle(90)
        self.people_id = 0

    def get_people_id(self):
        print("looking for people")
        p = self.people_id
        zone = 1
        while(self.people_id == p and zone<= 3):
            s = "EngagementZones/PeopleInZone"+str(zone)
            people_list = self.memory.getData(s)
            if( len(people_list)==1):
                self.people_id= people_list[0]
                print("new people(",self.people_id,") found:")
            elif( len(people_list)>1):
                self.people_id= people_list[0]
                print("More than one People in Zone",zone, " taking the first: ", self.people_id)
            else:
                zone += 1

    def onInput_onStart(self):
        print("Proximity Perceptioon Started...")
        self.get_people_id()
        while(1):
            people_list = self.memory.getData("EngagementZones/PeopleInZone1")
            people_list2 = self.memory.getData("EngagementZones/PeopleInZone2")
            people_list3 = self.memory.getData("EngagementZones/PeopleInZone3")
            if((self.people_id in people_list) or (self.people_id in people_list2) or (self.people_id in people_list3)):
                output_data["id"] = self.people_id
                s = "PeoplePerception/Person/"+ str(self.people_id) + "/Distance"
                output_data["dist"] = self.memory.getData(s)
                g = "PeoplePerception/Person/"+str(self.people_id)+"/IsLookingAtRobot" #key to get Gaze
                g1 = "PeoplePerception/Person/"+str(self.people_id)+"/LookingAtRobotScore" #key to get Gaze confidence level
                output_data["gaze"] = self.memory.getData(g)
                output_data["gaze_level"] = self.memory.getData(g1)
                #send distance to Impression Detection 
                print(output_data)
                file.write(str(datetime.now())+ str(output_data) + "\n")
                requests.post(url2+"/gaze_prox_perception", json=output_data)
            else:
                print("People(",self.people_id,") not visible looking for new id")
                self.get_people_id()
            time.sleep(5) #choose appropriate rate

PP_module = ProximityPerception()
PP_module.onInput_onStart()
    