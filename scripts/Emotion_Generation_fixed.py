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

class EmotionGenerator():
    def __init__(self) -> None:
        self.identity = [1,1,1] #identity in EPA space
        self.impression = [0,0,0] #impression in EPA space
        self.emotion = [0,0,0] #emotion in EPA space
        self.new_imp = False
        #self.new_emo = False
        self.time_decay = 5 #look for accurate data
        self.freq = 0
        self.delta = self.freq/self.time_decay
    
    #compute emotion evaluation
    def evaluation(self):
        """Positivity varies with the valence of one's transient impression"""
        sign = self.impression[0]/abs(self.impression[0])
        """Intensity varies with extremity of impression and fundamental meaning adjust it"""
        self.emotion[0] = self.impression[0] - self.identity[0]
        """fundamental activity and its impression effect positivity"""
        self.emotion[0] += (self.impression[2] -self.identity[2])*0.2
        """Saturate to max value of emotion"""
        if(abs(self.emotion[0]) > 4):
            self.emotion[0] = (self.emotion[0]/abs(self.emotion[0]))* 4

    #compute emotion potency
    def potency(self):
        """ Transient impression and fundamental power""" #RIVEDERE
        if(self.identity[1]< 0 and self.impression[1]-self.identity[1] > 1):
            #powerless but appear more power
            self.emotion[1] = self.impression[1]-self.identity[1]
        elif(self.identity[1]>0 and self.impression[1]-self.impression[1]<-1):
            #powerfull but appear less powerful   
            self.emotion[1] = self.impression[1]-self.identity[1]             
        """Activity affect potency"""
        self.emotion[1] += -(self.impression[2] - self.identity[2]) * 0.1 
        if(abs(self.emotion[1]) > 4):
            self.emotion[1] = (self.emotion[1]/abs(self.emotion[1]))* 4
    
    #compute emotion Activity
    def activity(self):
        """Comparison of transient and fundamental activity"""
        self.emotion[2] = self.impression [2] - self.identity[2] + 0.5
        if(abs(self.emotion[2]) > 4):
            self.emotion[2] = (self.emotion[2]/abs(self.emotion[2]))* 4

    def set_impression(self, imp):
        self.impression = imp

    def main(self):
        while(1):
            if(self.new_imp):
                self.evaluation()
                self.potency()
                self.activity()
            """else:
                #time decay
                for i in range(0,2):
                    self.emotion[i] = self.emotion[i] - self.delta
            """
            time.sleep(self.freq)

#Emotion Generation Node
emoNode = EmotionGenerator()

#REST API

app = Flask(__name__)

#Impression-EmotionGen Comunication
@app.route('/impression',methods =['POST'])
def get_impression():
    #receive impression from Impression Node
    print("Received Impression")
    #convert from json to array
    data = request.get_json()
    i = json.loads(data)
    emoNode.new_imp = True
    emoNode.set_impression(i)
    return jsonify({'succes':'True'}),200

#EmotionGen- EmotionExp Comunication
@app.route('/emotional_state',methods =['GET'])
def send_emotion():
    #request by Emotion Expression -> send emotion
    print("Received Request from Emotional expression")
    val = emoNode.new_emo
    emoNode.new_emo = False
    return jsonify({'new_emotion': val, 'emotion':emoNode.emotion}),200

#main
if __name__ == '__main__':
    #start the emotion Generation Node 
    threading.Thread(target=emoNode.main).start()
    #start restAPI server
    app.run(host='127.0.0.1', port=3000)
    