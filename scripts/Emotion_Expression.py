"""
Emotion Expression Component: get the emotion the robot feel in EPA space and perform one of the 5 it's able to feel.
From EPA found the closest one among the 5 he can display [Happy, Neutral, Sad, Anger and Fear].
Send the clue for the Expression to the Agent. 
Robot case: 
-Emotion Animation -> ALAnimationPlayerProxy 
-Eye LED color -> ALLeds
"""
import time
from naoqi import ALProxy
import random
import numpy as np 
from numpy.linalg import norm
import requests
import json

#basic emotion in EPA
emotion_map = {
    "H": np.array([3, 2.5, 2.8]),
    "N":np.array([0.01,0.01,0.01]),
    "F":np.array([-1.86, -2.2, 2.5]),
    "A":np.array([-2, 1.5, 2]),
    "SA":np.array([-3, -2.2 , -2.5]),
    "SU":np.array([0, 0, 3])}

#animations path for different emotions
happy_animation = [
    "H:path1",
    "H:path2",
    "H:path3",
    "H:path4",
    "H:path5"]

sad_animation = [
    "S:path1",
    "S:path2",
    "S:path3",
    "S:path4",
    "S:path5"]

angry_animation = [
    "A:path1",
    "A:path2",
    "A:path3",
    "A:path4",
    "A:path5"]

fear_animation = [
    "F:path1",
    "F:path2",
    "F:path3",
    "F:path4",
    "F:path5"]

#Pepper Connection
IP_ADD = "10.0.0.2" #set correct IP 
PORT = 9559 #set correct PORT 

url='http://127.0.0.1:3000/' #emotion Generation restAPI

#class
class EmotionExpression():
    def __init__(self, type):
        self.emotion = [0,0,0]
        self.emo_label = "N"
        self.time_decay = 10
        self.type = type
        self.new_emotion = False
        if type == 'R':
            print("Robot Case")
            self.animation_player = ALProxy("ALAnimationPlayerProxy", IP_ADD , PORT )
            self.leds = ALProxy("ALLeds",IP_ADD,PORT)
        else:
            #facial expression module
            print("Avatar Case")
    
        #client
    
    def get_basic(self):
        #get the basic emotion from the vector in EPA space 
        cos_list = []
        #compute cosine similarity 
        for key in emotion_map:
            #cos_list.append(cosine_similarity(self.emotion.reshape(1,-1), emotion_map[key].reshape(1,-1)))
            #print(key)
            cos_list.append(np.dot(self.emotion,emotion_map[key])/(norm(self.emotion)*norm(emotion_map[key])))
        print(cos_list)
        max_cos = 0.65
        index = 4
        #get higher cosine similarity 
        for i in range(0, len(cos_list)):
            if(cos_list[i] > max_cos):
                max_cos= cos_list[i]
                index = i
        #get label 
        keys = list(emotion_map.keys())
        self.emo_label = keys[index]
        print("basic emotion: "+ self.emo_label)

    def play_animation(self):
        #select random emotion
        r= random.randint(0,4)
        animation = "" 
        color = ""
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
        print("color: "+ color)
        print("animation: "+animation)
        #self.animation_player.run(animation,_async=True)
        #self.leds.fadeRGB("FaceLed", color, self.time_decay)

    def update_motion(self):
        print("Updating emotion behaviours")
        #find closest basic emotion
        self.get_basic()
        #select emotion to play
        if(self.type == "R"):
            if self.emo_label in ["H", "A", "F", "SA"] :
                print("play emotion:" + self.emo_label)
                self.play_animation()
            elif(self.emo_label == "N"):
                print("Neutral Emotional state")
            else:
                print("no able to dispaly emotion:" + self.emo_label)
        else:
            print("Avatar Case - emotion:" + self.emo_label)
            #face animation
    
    def get_emotion(self):
        print("Request Emotional State to Emotion Generator Node")
        #get request
        #convert json to array
        data = requests.get(url + '/emotional_state').json()
        self.new_emotion= data['new_emotion']
        if(self.new_emotion):
            print("received new emotion")
            self.emotion = data["emotion"]
            print(self.emotion)
        else:
            print("no new emotion")


#main
def main():
    emo_exp = EmotionExpression("A")
    print ("Emotion Expression Node")
    while(True):
        #get emotion
        emo_exp.get_emotion()
        """#to test without the other nodes 
        data = input("impression in EPA: ")
        i = []
        for val in data:
            i.append(float(val))
        emo_exp.new_emotion = True
        emo_exp.emotion = np.array(i)"""        
        #update motion if got a new one
        if(emo_exp.new_emotion):
          emo_exp.update_motion()
        #wait for emotion to decay
        time.sleep(emo_exp.time_decay)

main()
