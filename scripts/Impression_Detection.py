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

#basic emotions in EPA space
emotion_map = {
    "H":[3, 2.5, 2.8],
    "N":[0,0,0],
    "D":[-1.2,0,1],
    "F":[-1.86, -2.2, 2.5],
    "A":[-2, 1.5, 2],
    "SA":[-3, -2.2 , 2.5],
    "SU":[0, 0, 3]}
url='http://127.0.0.1:3000/' #emotion Generation API
#class
class ImpressionDetection():
    def __init__(self):
        self.impression = [0,0,0] #impression in EPA space
        self.user_emotion = [0,0,0] #user emotion in EPA
        self.proximity = 1 # proximity
        self.attention= 0 #user's attention
        #old value to get the transition
        self.old_emotion = [0,0,0] 
        self.old_prox = 1
        self.old_att = 0
        #delta to increment/decrement impressopm
        self.delta = 0.5
        #distance thresholds, try proximity with pepper and set this
        self.shorter_distance_th = 1.25 #Engagment Zone 1
        self.large_distance_th = 2 #Engagmente Zone 3
        #to set the sign of the new impression if positive or negative
        self.sign = [0,0,0]
        #value to start the processing of perception to get impression
        self.new_perc = False
        self.new_prox = False

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
        self.old_prox = self.proximity
        self.proximity = data

    def emotion_effects(self):
        #compute the effect of emotion in impresion making -> related to evaluation
        print("--------Emotion Effects--------")
        if(self.user_emotion[0]> 1 and self.user_emotion[0] - self.old_emotion[0] > 1):
            print("perceived good & better")
            #emozione migliorata in positivo
            self.impression[0] += self.delta * (self.user_emotion[0] - self.old_emotion[0])
            self.sign[0]= 1
        elif(self.user_emotion[0]< -1 and self.user_emotion[0] - self.old_emotion[0] <= -1):
            #emozione peggiorata in negativo
            print("perceived bad & worster")
            self.impression[0] += self.delta * (self.user_emotion[0] - self.old_emotion[0])
            self.sign[0] = -1
        else:
            if(self.user_emotion[0]!=0):
                self.sign[0] = self.user_emotion[0]/abs(self.user_emotion[0])
                print("perceived : " +str(self.sign[0]))
                self.impression[0] += self.sign[0]*0.1
            else: 
                self.sign[0] = 0 
        if abs(self.impression[0])>4:
            self.impression[0] = 4 * (self.impression[0]/abs(self.impression[0]))
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
                self.impression[2] += -(self.old_prox - self.proximity)
        
        else:
            self.sign[2] = 0
            #self.impression[2] += 0.1
        if abs(self.impression[2])>4:
            self.impression[2] = 4 * (self.impression[2]/abs(self.impression[2]))
        print("Impression: " + str(self.impression))

    def attention_effect(self):
        print("--------Attention Effects --------")
        #attention effect -> set Power and slightly increment/decremt the rest
        self.sign[1]= 0
        if(self.attention >= 0.5): 
            if(self.attention - self.old_att > 0.3):
                self.sign[1] = 1
                self.impression[1] += self.delta
            #increase effect of other
            self.impression[0] += self.sign[0]*0.1
            self.impression[1] += self.sign[1]*0.1
            self.impression[2] += self.sign[2]*0.1

        else:
            if(self.attention - self.old_att < -0.3):
                self.sign[1] = -1
                self.impression[1] += -self.delta
            #decrease the effect of others
            self.impression[0] += -self.sign[0]*0.1
            self.impression[1] += -self.sign[1]*0.1
            self.impression[2] += -self.sign[2]*0.1
        if abs(self.impression[1])>4:
            self.impression[1] = 4 * (self.impression[1]/abs(self.impression[1]))
        print("Impression: " + str(self.impression))

    def update_impression(self):
        #emotion effects
        upd = False
        if(self.new_perc):
            self.new_perc = False
            self.emotion_effects()
            self.attention_effect()
            upd = True
        if(self.new_prox):
            self.new_prox = False
            self.proximty_effects()
            upd = True
        #if new impression publish to EmoGen Node
        if(upd):
            print("Impression updated")
            print("Impression:"  + str(self.impression))
            data = json.dumps(self.impression)
            requests.post(url+'/impression' , json = data)      

    def main(self):
        print("Impression Detection Node")
        
        while(1):
            """#per test senza perception nodes
            data = input("morphcast string: ")
            imp_node.morphcast_feedback(data)
            data = float(input("proximity: "))
            imp_node.set_proximity(data)
            self.new_prox = True
            self.new_perc = True"""
            self.update_impression()
            time.sleep(3)

imp_node = ImpressionDetection()

#RestAPI
app = Flask(__name__)

@app.route('/morphcast_perception',methods =['POST'])
def get_emotion_attention():
    #receive attention and perception from Morphcat
    print("Received Morphcast")
    data = request.get_json()
    imp_node.new_perc = True
    print(str(data))
    imp_node.morphcast_feedback(json.loads(data))
    return jsonify({'succes':'True'}),200

@app.route('/proximity_perception',methods =['POST'])
def get_proximity():
    #received proximity
    print("Received Proximity")
    data = request.get_json()
    imp_node.new_prox = True
    print(data)
    imp_node.set_proximity(float(json.loads(data)))
    return jsonify({'succes':'True'}),200


if __name__ == '__main__':
    #start impression node main
    threading.Thread(target=imp_node.main).start()
    #start Rest API server.
    app.run(host='127.0.0.1', port=4000)
    #imp_node.main()