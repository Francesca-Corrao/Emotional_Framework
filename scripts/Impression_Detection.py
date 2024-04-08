""""
Impression Detection Component:
Get the information from the perception Module in order to get impression the user has of the robot.
Takes into account 3 different aspect:
-Emotion of the user [H,N,D,F,A, SA,SU]
-attention of the user [A/ NA]
-proximity []
from this enstablish an impression in the EPA plane
"""

#import
import time

#basic emotions in PAD space
emotion_map = {
    "H":[3, 2.5, 2.8],
    "N":[0,0,0],
    "D":[-1,0,1],
    "F":[-1.86, -2.2, 2.5],
    "A":[-2, 1.5, 2],
    "SA":[-3, -2.2 , 2.5],
    "SU":[0, 0, 3]}

#class
class ImpressionDetection():
    def __init__(self):
        self.impression = [0,0,0] #impression in EPA space
        self.user_emotion = [0,0,0]
        self.proximity = 1
        self.attention= 0.5
        self.old_emotion = [0,0,0]
        self.delta = 0.5
        #distance thresholds, try proximity with pepper and set this
        self.shorter_distance_th = 0.5
        self.large_distance_th = 1

    #get emotion and attention detected with morphcast
    def morphcast_feedback(self, data):
        #converti data
        d = data.split("_")
        #update old emotion
        self.old_emotion = self.user_emotion
        #update user emotion with the value in EPA space
        self.user_emotion = emotion_map[d[1]]
        #set user attention
        self.attention = float(d[0])

    #get proximity from Pepper
    def get_proximity(self, data):
        self.proximity = data

    def update_impression(self):
        #emotion effects
        print("emo_now:" + str(self.user_emotion[0]))
        print("emo_old:" +str(self.old_emotion[0]))
        if(self.user_emotion[0] >= 1 and self.old_emotion[0] <= -1):
            self.impression[0] = 1.5
        elif(self.user_emotion[0] <= -1 and self.old_emotion[0] >= 1):
            self.impression[0] = -1.5
        else:
            self.impression[0] = 0
        
        #proximity effect
        if(self.proximity <= self.shorter_distance_th):
            self.impression[2] = 1.5
            self.impression[0] = self.impression[0] + self.delta 
        elif(self.proximity >= self.large_distance_th):
            self.impression[2] = -1.5
            self.impression[0] -= self.delta

        #attention effect
        if(self.attention >= 0.5): 
            self.impression[1] = 1.5
            #increase effect of other 
        else:
            self.impression[1] = -1.5
            #decrease the effect of others
        print("impression: " + str(self.impression))       

        
#main
def main():
    imp_node = ImpressionDetection()
    #get morphcast string da tastiera
    while(1):
        data = input("morphcast string: ")
        imp_node.morphcast_feedback(data)
        data = float(input("proximity: "))
        imp_node.get_proximity(data)
        imp_node.update_impression()
        time.sleep(5)


main()