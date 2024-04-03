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

#basic emotions in PAD space
emotion_map = {
    "H":[3, 2.5, 2.8],
    "N":[0,0,0],
    "D":[-1,0,1],
    "F":[-1.86, -2.2, 2.5],
    "A":[-2, 1.5, 2],
    "SA":[-3, -2.2 , 2.5],
    "SU":[0, 0, 3],
}

#class
class ImpressionDetection():
    def __init__(self) -> None:
        self.impression = [0,0,0] #impression in EPA space
        self.user_emotion #emotion label [H,N,D,A,F,SA,SU]
        self.proximity #
        self.attention #attention label [A/NA]
        self.old_emotion
        self.old_impression #to keep into account a smooth transaction(?)
        self.delta = 0.1 #to update the impression based on the old one

    #get emotion and attention detected with morphcast
    def morphcast_feedback(self, data):
        #get emotion
        self.old_emotion = self.user_emotion
        self.user_emotion = emotion_map[data[emotion]]
        #get attention
        self.attention = data[attention]

    #get proximity from Pepper
    def get_proximity(self, data):
        self.proximity = data

    #update Impression
    def update_impression(self):
        #emotion effects
        if(self.user_emotion[1] >= 1 and self.old_emotion <= -1):
            self.impression[0] == 1.5
        elif(self.user_emotion <= -1 and self.old_emotion >= 1):
            self.impression[0] == -1.5
        else:
            self.impression[0] = 0
        
        #proximity effect
        if(self.proximity <= shorter_distance_th):
            self.impression[2] = 1.5
            self.impression[0] += self.delta 
        elif(self.get_proximity >= large_distance_th):
            self.impression[2] = -1.5
            self.impression[0] -= self.delta

        #attention effect
        if(self.attention == 'A'): 
            self.impression[1] = 1.5
            #increase effect of other 
        elif(self.attention == 'NA'):
            self.impression[1] = -1.5
            #decrease the effect of others       

        
#main