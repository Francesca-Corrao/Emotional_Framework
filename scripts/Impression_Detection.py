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
import time
from flask import Flask, request, jsonify 
import json
import requests
import threading

#rest API


#basic emotions in PAD space
emotion_map = {
    "H":[3, 2.5, 2.8],
    "N":[0,0,0],
    "D":[-1,0,1],
    "F":[-1.86, -2.2, 2.5],
    "A":[-2, 1.5, 2],
    "SA":[-3, -2.2 , 2.5],
    "SU":[0, 0, 3]}
url='http://127.0.0.1:3000/' #emotion Generation API
#class
class ImpressionDetection():
    def __init__(self):
        self.impression = [0,0,0] #impression in EPA space
        self.user_emotion = [0,0,0]
        self.proximity = 1 #change in proximity
        self.attention= 0
        self.old_emotion = [0,0,0]
        self.old_prox = 1
        self.old_att = 0
        self.delta = 1
        #distance thresholds, try proximity with pepper and set this
        self.shorter_distance_th = 0.5
        self.large_distance_th = 1
        self.sign = [0,0,0]
        self.new_perc = False
        self.new_prox = False

    #get emotion and attention detected with morphcast
    def morphcast_feedback(self, data):
        #converti data
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
        #change in proximity
        self.old_prox = self.proximity
        self.proximity = data

    def emotion_effects(self):
        
        print("--------Emotion Effects--------")
        if(self.user_emotion[0]> 1 and self.user_emotion[0] - self.old_emotion[0] > 1):
            print("perceived good & better")
            #emozione migliorata in positivo
            self.impression[0] += self.delta
            self.sign[0]= 1
        elif(self.user_emotion[0]< -1 and self.user_emotion[0] - self.old_emotion[0] < -1):
            #emozione peggiorata in negativo
            print("perceived bad & worster")
            self.impression[0] += -self.delta
            self.sign[0] = -1
        else:
            if(self.user_emotion[0]!=0):
                self.sign[0] = self.user_emotion[0]/abs(self.user_emotion[0])
                print("perceived : " +str(self.sign[0]))
                self.impression[0] += self.sign[0]*(0.1)
            else: 
                self.sign[0] = 0 
        print("impression: " + str(self.impression))

    def proximty_effects(self):
        print("--------Proximity Effects--------")
        #proximity effect
        if(self.proximity <= self.shorter_distance_th):
            self.impression[2] = 1.5
            self.sign[2] = 1
            if(self.proximity - self.old_prox <= -0.1):
                self.impression[0] +=  self.delta/3
                #self.impression[2] +=  self.delta

        elif(self.proximity <= self.large_distance_th):
            self.sign[2] = 0
        
        else:
            self.sign[2] = -1
            self.impression[2] = -1.5
            if(self.proximity - self.old_prox >= 0.1):
                self.impression[0] += -self.delta/3
        print("impression: " + str(self.impression))

    def attention_effect(self):
        print("--------Attention Effects --------")
        #attention effect
        self.sign[1]= 0
        if(self.attention >= 0.5): 
            if(self.attention - self.old_att > 0.15):
                self.sign[1] = 1
                self.impression[1] += self.delta
            #increase effect of other
            self.impression[0] += self.sign[0]*0.1
            self.impression[1] += self.sign[1]*0.1
            self.impression[2] += self.sign[2]*0.1

        elif(self.attention< 0.5):
            if(self.attention - self.old_att < -0.15):
                self.sign[1] = -1
                self.impression[1] += -self.delta
            #decrease the effect of others
            self.impression[0] += -self.sign[0]*0.1
            self.impression[1] += -self.sign[1]*0.1
            self.impression[2] += -self.sign[2]*0.1


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
        #post request to EmoGen Node
        if(upd):
            print("Impression updated")
            print("impression: " + str(self.impression))
            data = json.dumps(self.impression)
            requests.post(url+'/impression' , json = data)      

    def main(self):
        #get morphcast string da tastiera
        while(1):
            #data = input("morphcast string: ")
            #imp_node.morphcast_feedback(data)
            #data = float(input("proximity: "))
            #imp_node.get_proximity(data)
            self.update_impression()
            time.sleep(3)

imp_node = ImpressionDetection()
app = Flask(__name__)
@app.route('/morphcast_perception',methods =['POST'])
def get_emotion_attention():
    #receive impression from Impression Node
    print("Received Morphcast")
    #convert json to 
    data = request.get_json()
    imp_node.new_perc = True
    print(str(data))
    imp_node.morphcast_feedback(json.loads(data))
    return jsonify({'succes':'True'}),200

@app.route('/proximity_perception',methods =['POST'])
def get_proximity():
    print("Received Proximity")
    data = request.get_json()
    imp_node.new_prox = True
    print(data)
    imp_node.set_proximity(float(json.loads(data)))
    return jsonify({'succes':'True'}),200


if __name__ == '__main__':
    threading.Thread(target=imp_node.main).start()
    app.run(host='127.0.0.1', port=4000)