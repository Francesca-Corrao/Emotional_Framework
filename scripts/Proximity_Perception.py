from naoqi import ALProxy
import time
#localhost:51260
#pepper.local.:9559
IP_ADD = "10.0.0.2"
PORT = 9559
class ProximityPerception():
    def __init__(self):
        self.memory = ALProxy("ALMemory", IP_ADD, PORT) #aggiungere IP e porta
        self.people_perception = ALProxy("ALPeoplePerception", IP_ADD,PORT) #aggiungere IP e porta
        self.engagment_zone = ALProxy("ALEngagementZones",IP_ADD,PORT) #aggiungere IP e porta 
        self.engagment_zone.setFirstLimitDistance(1) 
        self.engagment_zone.setSecondLimitDistance(2)
        self.engagment_zone.setLimitAngle(90)
        self.people = False
        self.people_id = []

    def onInput_onStart(self):
        print("Start")
        while(True):
            self.people_id = []
            people_list = self.memory.getData("EngagementZones/PeopleInZone1")
            if len(people_list) >0:
                self.people = True
                for p in people_list:
                    print(p)
                    s = "PeoplePerception/Person/"+ str(p) + "/Distance"
                    self.people_id.append(s) 
            else:
                people_list = self.memory.getData("EngagementZones/PeopleInZone2")
                if len(people_list) >0:
                    self.people = True
                    for p in people_list:
                        print(p)
                        s = "PeoplePerception/Person/"+ str(p) + "/Distance"
                        self.people_id.append(s)

            if(self.people):
                for p in self.people_id:
                    dist = self.memory.getData(p)
                    print(p, " : ", dist)
            else:
                print("no People detected")
            time.sleep(3)
        pass


print("HEllo world!")
PP_module = ProximityPerception()
PP_module.onInput_onStart()



