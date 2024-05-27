""""
Impression Detection Component:
Get the information from the perception Module in order to get impression the user has of the robot.
Takes into account 3 different aspect, collect by the rest API:
-Emotion of the user [H,N,D,F,A,SA,SU]
-attention of the user [0-1]
-proximity []
from this enstablish an impression in the EPA plane
Then the impression is send to the Emotion Generation Node.
"""

#import
import time
from flask import Flask, request, jsonify 
import json
import requests
import threading
from datetime import datetime

MORPHCAST_TH = 2
PORT = 4000
#basic emotions in EPA space
emotion_map = {
    "H":[3, 2.5, 2.8],
    "N":[0,0,0],
    "D":[-1.2,0,1],
    "F":[-1.86, -2.2, 2.5],
    "A":[-2, 1.5, 2],
    "SA":[-3, -2.2 , 2.5],
    "SU":[0, 0, 3]}
url='http://127.0.0.1:3000/' #Emotion Generation API

#class
class ImpressionDetection():
    def __init__(self):
        self.impression = [0,0,0] #impression in EPA space
        self.user_emotion = [0,0,0] #user emotion in EPA
        self.proximity = 1 # proximity
        self.attention= 0 #user's attention
        self.choice_impression = [0,0,0]
        #old value to get the transition
        self.old_emotion = [0,0,0] 
        self.old_prox = 1
        self.old_att = 0
        #delta to increment/decrement impression
        self.delta = 0.5
        #distance thresholds, try proximity with pepper and set this 
        self.shorter_distance_th = 1.25 #Engagment Zone 1
        self.large_distance_th = 2 
        #to set the sign of the new impression if positive or negative
        self.sign = [0,0,0]
        #value to start the processing of perception to get impression
        self.new_emo = False
        self.new_att = False
        self.new_prox = False
        self.new_choice = False

    #get emotion and attention detected with morphcast
    def morphcast_feedback(self, data):
        #data conversion
        d = data.split("_")
        #update old emotion
        self.old_emotion = self.user_emotion
        #update user emotion with the value in EPA space
        self.user_emotion = emotion_map[d[1]]
        #set user attention
        self.old_att = self.attention
        self.attention = float(d[0])

    #get proximity from Pepper
    def set_proximity(self, data):
        self.new_prox = True
        self.old_prox = self.proximity
        self.proximity = data

    def set_attention(self, data):
        self.new_att = True
        self.old_att = self.attention
        self.attention = data["gaze_level"]*data["gaze"]
        print(self.attention)
    
    def set_choice(self, data):
        self.choice_impression = json.loads(data)

    def saturate_allimpression(self):
        for i in range(0,3):
            if abs(self.impression[i])>4:
                self.impression[i] = 4 * (self.impression[i]/abs(self.impression[i]))
    
    def saturate_impression(self, index):
        if abs(self.impression[index])>4:
            self.impression[index] = 4 * (self.impression[index]/abs(self.impression[index]))

    def emotion_effects(self):
        #compute the effect of emotion in impresion making -> related to evaluation
        print("--------Emotion Effects--------")
        if(self.user_emotion[0]> 1 and self.user_emotion[0] - self.old_emotion[0] > 1):
            #emozione migliorata in positivo
            self.impression[0] += self.delta * (self.user_emotion[0] - self.old_emotion[0])
            self.sign[0]= 1
        elif(self.user_emotion[0]< -1 and self.user_emotion[0] - self.old_emotion[0] <= -1):
            #emozione peggiorata in negativo
            self.impression[0] += self.delta * (self.user_emotion[0] - self.old_emotion[0])
            self.sign[0] = -1
        else:
            if(self.user_emotion[0]!=0):
                self.sign[0] = self.user_emotion[0]/abs(self.user_emotion[0])
                self.impression[0] += self.sign[0]*0.1
            else: 
                self.sign[0] = 0 
        self.saturate_impression(0)
        print("Impression: " + str(self.impression))

    def proximty_effects(self):
        print("--------Proximity Effects--------")
        #proximity effect on Impression makig -> Activity and Evaluation 
        if(self.proximity <= self.shorter_distance_th):
            self.impression[2] += 0.2
            self.sign[2] = 1
            if(self.proximity - self.old_prox <= -0.25):
                self.impression[2] += self.old_prox - self.proximity
                self.impression[0] +=  self.delta/2

        elif(self.proximity >= self.large_distance_th):
            self.sign[2] = -1
            self.impression[2] += -0.2
            if(self.proximity - self.old_prox >= 0.25):
                self.impression[0] += -self.delta/2
                self.impression[2] += (self.old_prox - self.proximity)
        
        else:
            self.sign[2] = 0
            self.impression[2] += 0.5*(self.old_prox - self.proximity)
        self.saturate_impression(2)
        print("Impression: " + str(self.impression))

    def attention_effect(self):
        print("--------Attention Effects --------")
        #attention effect -> set Power and slightly increment/decremt the rest
        if(self.attention >= 0.5): 
            self.sign[1] = 1
            if(self.attention - self.old_att > 0.3):
                self.impression[1] += self.delta
            #increase effect of other
            self.impression[0] += self.sign[0]*self.attention*0.1 #the more user look the more it'll increment
            self.impression[1] += self.sign[1]*self.attention*0.1
            self.impression[2] += self.sign[2]*self.attention*0.1

        else:
            self.sign[1] = -1
            if(self.attention - self.old_att < -0.3):
                self.impression[1] += -self.delta
            #decrease the effect of others
            self.impression[0] += -self.sign[0]*(1-self.attention)*0.1 #the less it look the more it'll decrement
            self.impression[1] += self.sign[1]*(1-self.attention)*0.1
            self.impression[2] += -self.sign[2]*(1-self.attention)*0.1
        self.saturate_impression(1)
        print("Impression: " + str(self.impression))

    def choice_effects(self):
        print("--------Choice Effects --------")
        for i in range(0,3):
            if(self.choice_impression[i] == self.sign[i]):
                self.impression[i] += 2*self.sign[1]*self.delta
            else:
                self.impression[i] += self.choice_impression[i]*self.delta
                # set sign to be the same of choice_impression per ora forse meglio di no
        self.saturate_allimpression()
        print("Impression: " + str(self.impression))

    def update_impression(self):
        #emotion effects
        upd = False
        if(self.new_emo and self.proximity<MORPHCAST_TH):
            self.new_emo = False
            self.emotion_effects()
            self.attention_effect()
            upd = True
        elif(self.new_att):
            self.new_att = False
            self.attention_effect()
            upd = True
        if(self.new_prox):
            self.new_prox = False
            self.proximty_effects()
            upd = True
        if(self.new_choice):
            self.new_choice = False
            self.choice_effects()
            upd = True
        #if new impression publish to EmoGen Node
        if(upd):
            print(datetime.now(), "Impression updated ")
            data = json.dumps(self.impression)
            requests.post(url+'/impression' , json = data)      

    def main(self):
        print("Impression Detection Node")
        while(1):
            self.update_impression()

imp_node = ImpressionDetection()

#RestAPI
app = Flask(__name__)

@app.route('/morphcast_perception',methods =['POST'])
def get_emotion_attention():
    #receive attention and perception from Morphcat
    print("Received Morphcast")
    data = request.get_json()
    imp_node.new_emo = True
    imp_node.morphcast_feedback(json.loads(data))
    return jsonify({'succes':'True'}),200

@app.route('/proximity_perception',methods =['POST'])
def get_proximity():
    #received proximity
    print("Received Proximity")
    data = request.get_json()
    imp_node.new_prox = True
    imp_node.set_proximity(float(json.loads(data)))
    return jsonify({'succes':'True'}),200

@app.route('/gaze_prox_perception',methods =['POST'])
def get_gazeprox():
    #received proximity
    print("Received Gaze and Proximity")
    data = request.get_json()
    imp_node.set_proximity(float(data["dist"]))
    imp_node.set_attention(data)
    return jsonify({'succes':'True'}),200

@app.route('/choice_impression', methods= ['POST'])
def get_choice():
    print("Received Choice Impression")
    data = request.get_json()
    imp_node.new_choice = True
    print(data)
    imp_node.set_choice(data)
    return jsonify({'succes':'True'}),200

if __name__ == '__main__':
    print("Impression Detection")
    #start impression node main
    threading.Thread(target=imp_node.main).start()
    #start Rest API server.
    app.run(host='127.0.0.1', port=PORT)