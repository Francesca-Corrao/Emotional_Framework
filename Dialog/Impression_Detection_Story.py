""""
Impression Detection Component:
Get the information from the perception Module in order to get impression the user has of the robot.
Takes into account 4 different aspect, collect by the rest API:
- Emotion of the user [H,N,D,F,A,SA,SU]
- Attention of the user [0-1]
- Proximity[0-2.5]
- Story's choice related impression in EPA space
from this enstablish an impression in the EPA space
Then the impression is send to the Emotion Generation Node.
"""

#import
import time
from flask import Flask, request, jsonify 
import json
import requests
import threading
from datetime import datetime

MORPHCAST_TH = 1.5
PORT = 4000
#basic emotions in EPA space
emotion_map = {
    "H":[3, 0.8, 0.5],
    "N":[0,0,0],
    "D":[-1.5,0.2,-2],
    "F":[-0.6, -2.1, 2.1],
    "A":[-2, 2.8, 1],
    "SA":[-0.8, -1.9 , -1.9],
    "SU":[0.5, -0.4, 1]}
url='http://127.0.0.1:3000/' #Emotion Generation API

morphcast_active = False

file_emotion="../test/impression.txt"
file = open(file_emotion, 'a')
file.write("Start ..." + str(datetime.now()) + "\n")
#class
class ImpressionDetection():
    def __init__(self):
        self.impression = [0,0,0] #impression in EPA space
        self.user_emotion = [0,0,0] #user emotion in EPA
        self.proximity = 2.5 # proximity
        self.attention= 0 #user's attention
        self.choice_impression = [0,0,0]
        #old value to get the transition
        self.old_emotion = [0,0,0] 
        self.old_prox = self.proximity
        self.old_att = self.attention
        #delta to increment/decrement impression
        self.delta = 0.5
        #distance thresholds
        self.shorter_distance_th = 1 #Engagment Zone 1
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
        self.old_emotion = self.user_emotion
        self.user_emotion = emotion_map[d[1]]
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
        #effect of emotion -> evaluation
        global file
        file.write("--------Emotion Effects--------"+"\n")
        if(self.user_emotion[0]> 1 and self.user_emotion[0] - self.old_emotion[0] > 1):
            self.impression[0] += self.delta * (self.user_emotion[0] - self.old_emotion[0])
            self.sign[0]= 1
        elif(self.user_emotion[0]< -1 and self.user_emotion[0] - self.old_emotion[0] <= -1):
            self.impression[0] += self.delta * (self.user_emotion[0] - self.old_emotion[0])
            self.sign[0] = -1
        else:
            if(self.user_emotion[0]!=0):
                self.sign[0] = self.user_emotion[0]/abs(self.user_emotion[0])
                self.impression[0] += self.sign[0]*0.1
            else: 
                self.sign[0] = 0 
        self.saturate_impression(0)
        file.write("Impression: " + str(self.impression)+"\n")
        file.flush

    def proximty_effects(self):
        global file
        file.write("--------Proximity Effects--------\n")
        #proximity effect -> Activity and Evaluation 
        if(self.proximity <= self.shorter_distance_th):
            self.impression[2] += 0.2
            self.sign[2] = 1
            if(self.proximity - self.old_prox <= -0.5):
                self.impression[2] += self.old_prox - self.proximity
                self.impression[0] +=  self.delta/2

        elif(self.proximity >= self.large_distance_th):
            self.sign[2] = -1
            self.impression[2] += -0.2
            if(self.proximity - self.old_prox >= 0.5):
                self.impression[0] += -self.delta/2
                self.impression[2] += (self.old_prox - self.proximity)
        
        else:
            print("else:", self.old_prox - self.proximity)
            self.sign[2] = 0
            self.impression[2] += 0.5*(self.old_prox - self.proximity)
        self.saturate_impression(2)
        file.write("Impression: " + str(self.impression)+"\n")
        file.flush

    def attention_effect(self):
        global file
        file.write("--------Attention Effects --------\n")
        #attention effect -> Power and slightly increment/decremt the rest
        if self.attention != self.old_att:
            if(self.attention >= 0.5): 
                self.sign[1] = 1
                self.impression[0] += self.sign[0]*self.attention*0.1 #the more user look the more it'll increment
                self.impression[1] += self.sign[1]*self.attention*0.1
                self.impression[2] += self.sign[2]*self.attention*0.1
            else:
                self.sign[1] = -1
                self.impression[0] += -self.sign[0]*(1-self.attention)*0.1 #the less it look the more it'll decrement
                self.impression[1] += self.sign[1]*(1-self.attention)*0.1
                self.impression[2] += -self.sign[2]*(1-self.attention)*0.1
            self.saturate_impression(1)
            file.write("Impression: " + str(self.impression)+"\n")
            file.flush

    def choice_effects(self):
        global file
        file.write("--------Choice Effects --------")
        for i in range(0,3):
            print(self.choice_impression[i])
            if(self.choice_impression[i] == self.sign[i]):
                self.impression[i] = self.sign[i]
            else:
                self.impression[i] = self.choice_impression[i]
        self.saturate_allimpression()
        file.write("Impression: " + str(self.impression)+"\n")
        file.flush

    def update_impression(self):
        global morphcast_active, file
        upd = False
        if(self.new_choice):
            self.new_choice = False
            self.choice_effects()
            upd = True
        if(self.new_prox):
            self.new_prox = False
            self.proximty_effects()
            upd = True
        if(self.new_emo and self.proximity<MORPHCAST_TH):
            self.new_emo = False
            self.emotion_effects()
            self.attention_effect()
            upd = True
        elif(self.new_att):
            self.new_att = False
            morphcast_active = False
            self.attention_effect()
            upd = True
        #if new impression publish to EmoGen Node
        if(upd):
            print(datetime.now(), "Impression updated: "+ str(self.impression))
            file.write(str(datetime.now())+ " Impression updated: "+ str(self.impression) + "\n")
            data = json.dumps(self.impression)
            requests.post(url+'/impression' , json = data)
            file.flush()

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
    global morphcast_active
    data = request.get_json()
    imp_node.new_emo = True
    morphcast_active = True
    imp_node.morphcast_feedback(json.loads(data))
    return jsonify({'succes':'True'}),200

@app.route('/proximity_perception',methods =['POST'])
def get_proximity():
    #received proximity
    data = request.get_json()
    imp_node.new_prox = True
    imp_node.set_proximity(float(json.loads(data)))
    return jsonify({'succes':'True'}),200

@app.route('/gaze_prox_perception',methods =['POST'])
def get_gazeprox():
    #received proximity
    data = request.get_json()
    imp_node.set_proximity(float(data["dist"]))
    if not(morphcast_active) or imp_node.proximity >= MORPHCAST_TH :
        imp_node.set_attention(data)
    return jsonify({'succes':'True'}),200

@app.route('/choice_impression', methods= ['POST'])
def get_choice():
    #received choice
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