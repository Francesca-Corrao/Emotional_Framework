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
import sys
from datetime import datetime

#basic emotion in EPA
emotion_map = {
    "H": np.array([3, 0.8, 1]),
    "F":np.array([-0.6, -2.1, 2.1]),
    "A":np.array([-2.2, 2.8, 1]),
    "SA":np.array([-1.5, -1.9 , -1.9])
    }

#animations path for different emotions
happy_animation = [
    'emotions-8fe336/Happy_1',
    'emotions-8fe336/Happy_2']

sad_animation = [
    'emotions-8fe336/Sad_1',
    'emotions-8fe336/Sad_2']

angry_animation = [
    'emotions-8fe336/Anger_2',
    'emotions-8fe336/Anger_4']

fear_animation = [
    'emotions-8fe336/Fear_1',
    'emotions-8fe336/Fear_2']

#Pepper Connection
IP_ADD = "10.0.0.6" #set correct IP 
PORT = 9559 #set correct PORT 

url='http://127.0.0.1:3000/' #emotion Generation restAPI
file_emotion = "../test/expression.txt"
file = open(file_emotion, "a")
file.write("Beging" + str(datetime.now()) + "\n")
#class
class EmotionExpression():
    def __init__(self, type):
        self.emotion = [0,0,0]
        self.emo_label = "N"
        self.old_emotion = " "
        self.time_decay = 30.0
        self.type = type
        self.new_emotion = False
        self.end_time = time.time()
        if type == 'R':
            print("Robot Case")
            self.animation_player = ALProxy("ALAnimationPlayer", IP_ADD , PORT )
            self.leds = ALProxy("ALLeds",IP_ADD,PORT)
            self.leds.fadeRGB("FaceLeds", "white", 5.0)
        elif type == 'A':
            #facial expression module
            print("Avatar Case")
    
    def get_basic(self):
        global file
        #get the basic emotion from the vector in EPA space 
        cos_list = []
        #compute cosine similarity 
        for key in emotion_map:
            cos_list.append(np.dot(self.emotion,emotion_map[key])/(norm(self.emotion)*norm(emotion_map[key])))
            file.write(str(key) + ":"+ str(cos_list[-1])+ "\n") #da errorreeee
        max_cos = 0.6
        index = -1
        #get higher cosine similarity 
        for i in range(0, len(cos_list)):
            if(cos_list[i] > max_cos):
                max_cos= cos_list[i]
                index = i
        #get label 
        if index != -1 :
            keys = list(emotion_map.keys())
            self.emo_label = keys[index]
        else:
            self.emo_label = " N "
        file.write("basic emotion: "+ self.emo_label + "\n")
        file.flush()

    def play_animation(self):
        #select random animation index
        r= random.randint(0,1)
        animation = "" 
        color = ""
        if(self.emo_label == "H"):
            print("Happy")
            animation = happy_animation[r]
            color = 0x55ff00
        elif(self.emo_label == "SA"):
            print("Sad")
            animation = sad_animation[r]
            color = 0x0000ff 
        elif(self.emo_label == "A"):
            print("Angry")
            animation = angry_animation[r]
            color = 0xeb0000
        elif(self.emo_label == "F"):
            print("Fear")
            animation= fear_animation[r]
            color = 0x000000
        self.leds.fadeRGB("FaceLeds", color, 1.0, _async = True)
        if(self.old_emotion == self.emo_label and time.time() <= self.end_time):
            return
        else:
            self.animation_player.run(animation)
            self.end_time = time.time()+self.time_decay
        

    def update_motion(self):
        print("Updating emotion behaviours")
        #find closest basic emotion
        self.old_emotion = self.emo_label
        self.get_basic()
        #run animation
        if(self.type == "R"):
            if self.emo_label in ["H", "A", "F", "SA"] :
                print("play emotion:" + self.emo_label)
                self.play_animation()
            elif(self.emo_label == "N"):
                print("Neutral Emotional state")
                self.leds.fadeRGB("FaceLeds", "white", 0.5)
            else:
                print("no able to dispaly emotion:" + self.emo_label)
        else:
            print("Avatar Case - emotion:" + self.emo_label)
            #face animation
    
    def get_emotion(self):
        global file
        file.write(str(datetime.now()) + "Request Emotional State to Emotion Generator Node\n")
        data = requests.get(url + 'emotional_state').json() 
        if(data['new_emotion']):
            self.emotion = data["emotion"]
            print("received new emotion:", self.emotion)
            self.new_emotion= data['new_emotion']
        else:
            self.new_emotion= data['new_emotion']
            print("no new emotion")
        
    def input_emotion(self):
        data = input("impression in EPA: ")
        i = []
        for val in data:
            i.append(float(val))
        self.new_emotion = True
        self.emotion = np.array(i)

#main
    def main(self):
        print ("Emotion Expression Node")
        while(True):       
            #update motion if got a new emotion
            if(self.new_emotion):
                self.new_emotion = False
                self.update_motion()

#emo = EmotionExpression("A")
#emo.input_emotion()
#emo.update_motion()