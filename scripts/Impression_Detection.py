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
    def morphcast_feedback(self):
        #get emotion
        self.user_emotion
        #get attention
        self.attention

    #get proximity from Pepper
    def get_proximity(self):
        self.proximity

    #update Impression
    def update_impression(self):
        #evaluation according to user emotion
        if(self.user_emotion == good and self.old_emotion == bad):
            self.impression[0] == good
            if(self.attention == 'A'):
                self.impression[0] += self.delta
        elif(self.user_emotion == bad and self.old_emotion == good):
            self.impression[0] == bad
            if(self.attention == 'A'):
                self.impression[0] -= self.delta
        else:
            self.impression[0] = neutral
        
        #proximity effect
        if(self.proximity <= shorter_distance_th):
            self.impression[2] = active
            self.impression[0] += self.delta 
        elif(self.get_proximity >= large_distance_th):
            self.impression[2] = passive
            self.impression[0] -= self.delta

        #attention effect
        if(self.attention == 'A'): 
            self.impression[1] = power
        elif(self.attention == 'NA'):
            self.impression[1] = powerless        

        
#main