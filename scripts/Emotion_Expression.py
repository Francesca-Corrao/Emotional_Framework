"""
Emotion Expression Component: get the emotion the robot feel in EPA space and perform one of the 5 it's able to feel.
From EPA found the closest one among the 5 he can display [Happy, Neutral, Sad, Anger and Fear].
Send the clue for the Expression to the Agent. 
It takes into account the time decay of emotions and the fact that the transition should be smooth. 
"""

from sklearn.metrics.pairwise import cosine_similarity
import time
from naoqi import ALProxy
#basic emotion in EPA
emotion_map = {
    "H":[3, 2.5, 2.8],
    "N":[0,0,0],
    "D":[-1,0,1],
    "F":[-1.86, -2.2, 2.5],
    "A":[-2, 1.5, 2],
    "SA":[-3, -2.2 , 2.5],
    "SU":[0, 0, 3]}

happy_animation = [
    "path1",
    "path2",
    "path3",
    "path4",
    "path5"]

sad_animation = [
    "path1",
    "path2",
    "path3",
    "path4",
    "path5"]

angry_animation = [
    "path1",
    "path2",
    "path3",
    "path4",
    "path5"]

fear_animation = [
    "path1",
    "path2",
    "path3",
    "path4",
    "path5"]

IP_ADD = "10.0.0.2" #set correct IP 
PORT = 9559 #set correct PORT 

#class
class EmotionExpression():
    def __init__(self, type):
        self.emotion = [0,0,0]
        self.emo_label = "N"
        self.time_decay = 4
        self.type = type
        if type == 'R':
            print("Robot Case")
            self.animation_player = ALProxy("ALAnimationPlayerProxy", IP_ADD , PORT )
            self.leds = ALProxy("ALLeds",IP_ADD,PORT)
        else:
            #facial expression module
            print("Avatar")
    
        #client
    
    def get_basic(self):
        cos_list = []
        #compute cosine similarity 
        for key in emotion_map:
            cos_list.append(cosine_similarity(self.emotion, emotion_map[key]))
        max_cos = 0
        index = 0
        #get higher cosine similarity 
        for i in len(cos_list):
            if(cos_list[i]>max_cos):
                max_cos= cos_list[i]
                index = i
        
        #get label 
        self.emo_label = emotion_map.key(index)

    def play_animation(self):
        #select random emotion
        r= 0
        animation, color
        if(self.emo_label == "H"):
            print("Happy")
            animation = happy_animation[r]
            color = "yellow" #sostituire con HEX
        elif(self.emo_label == "S"):
            print("Sad")
            animation = sad_animation[r]
            color = "blue" #sostituire con HEX
        elif(self.emo_label == "A"):
            print("Angry")
            animation = angry_animation[r]
            color = "red"
        else:
            print("Fear")
            animation= fear_animation[r]
            color = "purple"

        #self.animation_player.run(animation,_async=True)
        #self.leds.fadeRGB("FaceLed", color, self.time_decay)

    def update_motion(self):
        print("Updating emotion behaviours")
        #request emotion
        #find closest basic emotion
        self.get_basic()
        #select emotion to play
        if(self.type == "R"):
            if self.emo_label in ["H", "A", "F", "S"] :
                print("play emotion:" + self.emo_label)
                #python perchè non hai gli switch !!!!!
                self.play_animation()
            elif(self.emo_label == "N"):
                print("Neutral Emotional state")
            else:
                print("no able to dispaly emotion:" + self.emo_label)
        else:
            print("Avatar Case")
            #face animation
        time.sleep(self.time_decay/2)

         
#main
def main():
    emo_exp = EmotionExpression()
    while(True):
        emo_exp.update_motion()
    

main()
