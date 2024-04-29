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
        dist = MAX_DIST
        self.get_people_id()
        while(1):
            #people_list = self.memory.getData("EngagementZones/PeopleInZone1")
            #people_list2 = self.memory.getData("EngagementZones/PeopleInZone2")
            #people_list3 = self.memory.getData("EngagementZones/PeopleInZone3")
            #print(people_list)
            #if((self.people_id in people_list) or (self.people_id in people_list2) or (self.people_id in people_list3)):
            if (self.memory.getData("PeoplePerception/Person/"+str(self.people_id)+"/IsVisible")):
                print("people(",self.people_id,") still visible")
                s = "PeoplePerception/Person/"+ str(self.people_id) + "/Distance"
                dist = self.memory.getData(s)
                g = "PeoplePerception/Person/"+str(self.people_id)+"/IsLookingAtRobot" #key to get Gaze
                g1 = "PeoplePerception/Person/"+str(self.people_id)+"/LookingAtRobotScore" #key to get Gaze confidence level
                gaze = self.memory.getData(g)
                gaze_level = self.memory.getData(g1)
                #send distance to Impression Detection 
                print(self.people_id, "  DIST : ", dist)
                print("GAZE: ", gaze," level :", gaze_level)
                data2 = json.dumps(dist)
                requests.post(url2+"/proximity_perception", json=data2)
            else:
                print("People(",self.people_id,") not visible looking for new id")
                self.get_people_id()
            time.sleep(3) #choose appropriate rate

    def Gaze(self):
        while(1):
            g = "PeoplePerception/Person/"+str(self.people_id)+"/IsLookingAtRobot" #key to get Gaze
            g1 = "PeoplePerception/Person/"+str(self.people_id)+"/LookingAtRobotScore" #key to get Gaze confidence level
            gaze = self.memory.getData(g)
            gaze_level = self.memory.getData(g1)
            print(gaz)


PP_module = ProximityPerception()
PP_module.onInput_onStart()
    