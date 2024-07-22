"""
FIXED EMOTION GENERATED WHEN RECEIVE A NEW IMPRESSION
Emotion Generation Component: take as input the impressione the human has of the agent 
and produce the emotion the robot should feel according to the Affect Control Theory.
Three main components, each computing one of the value of the emotion in the EPA space:
-Evaluation 
-Potency 
-Activity
"""
from flask import Flask, request, jsonify 
#import request 
import threading
import json
import time
from datetime import datetime

PORT = 3000
file_emotion = "../test/emotion.txt"
file = open(file_emotion, "a")
file.write("Beging" + str(datetime.now()) + "\n")

class EmotionGenerator():
    def __init__(self):
        self.identity = [1,1.1,0.9] #identity in EPA space
        self.impression = [0,0,0] #impression in EPA space
        self.emotion = [0,0,0] #emotion in EPA space
        self.new_imp = False
        self.new_emo = False
    
    #compute emotion evaluation
    def evaluation(self):
        self.emotion[0] = self.impression[0] - self.identity[0] + 1        
        self.emotion[0] += (self.impression[2] -self.identity[2])*0.2
        if(abs(self.emotion[0]) > 4):
            self.emotion[0] = (self.emotion[0]/abs(self.emotion[0]))* 4

    #compute emotion potency
    def potency(self):
        if(self.identity[1]< 0 and self.impression[1]-self.identity[1] > 1):
            self.emotion[1] = self.impression[1]-self.identity[1]
        elif(self.identity[1]>0 and self.impression[1]-self.identity[1]<=-1):  
            self.emotion[1] = self.impression[1]-self.identity[1]
        else: 
            self.emotion[1] = self.impression[1]       
        self.emotion[1] += -(self.impression[2] - self.identity[2])
        if(abs(self.emotion[1]) > 4):
            self.emotion[1] = (self.emotion[1]/abs(self.emotion[1]))* 4 


    #compute emotion Activity
    def activity(self):        
        self.emotion[2] = self.impression [2] + self.identity[2]
        if(abs(self.emotion[2]) > 4):
            self.emotion[2] = (self.emotion[2]/abs(self.emotion[2]))* 4

    def set_impression(self, imp):
        self.impression = imp

    def main(self):
        global file
        print("Emotion Generation Node")
        while(1):
            if(self.new_imp):
                self.new_imp = False
                print(self.impression)
                self.evaluation()
                self.potency()
                self.activity()
                self.new_emo = True
                print(datetime.now(), " Emotion Updated : ", self.emotion)
                file.write(str(datetime.now()) + "Emotion Updated: "+ str(self.emotion)+"\n")
                file.flush()
            time.sleep(self.freq)

#Emotion Generation Node
emoNode = EmotionGenerator()

#REST API
app = Flask(__name__)

#Impression-EmotionGen Comunication
@app.route('/impression',methods =['POST'])
def get_impression():
    data = request.get_json()
    i = json.loads(data)
    emoNode.new_imp = True
    emoNode.set_impression(i)
    return jsonify({'succes':'True'}),200

#EmotionGen- EmotionExp Comunication
@app.route('/emotional_state',methods =['GET'])
def send_emotion():
    print("Received Request from Emotional expression")
    val = emoNode.new_emo
    emoNode.new_emo = False
    return jsonify({'new_emotion': val, 'emotion':emoNode.emotion}),200

#main
if __name__ == '__main__':
    #start the emotion Generation Node 
    threading.Thread(target=emoNode.main).start()
    #start restAPI server
    app.run(host='127.0.0.1', port=PORT)
    