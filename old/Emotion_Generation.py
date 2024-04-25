""" Emotion Generation Component: take as input the impressione the human has of the agent 
and produce the emotion the robot should feel according to the Affect Control Theory.
Three main components, each computing one of the value of the emotion in the EPA space:
-Evaluation 
-Potency 
-Activity
"""

#import needed
from flask import Flask, request, jsonify 
#import request 
import threading
import json
import time

#restAPI
app = Flask(__name__)

#EmotionGeneration class
class EmotionGenerator:
    def __init__(self) -> None:
        self.identity = [1,1,1] #identity in EPA space
        self.impression = [0,0,0] #impression in EPA space
        self.emotion = [0,0,0] #emotion in EPA space
        self.new_imp = False
        self.new_emo = False

    #computation of emotion evaluation
    def evaluation(self):
        print("-------- Evaluation Computation --------")
    
        #positivity varies directly with valence of impression
        sign = int(self.impression[0]/abs(self.impression[0]))
        #intensity varies with identity evaluation
        val = abs(-self.identity[0]+self.impression[0]+sign*1) #da sistemare
        self.emotion[0] += sign * val * 0.5 
        #positivity related to identity activity
        if(self.identity[2]<0):
            self.emotion[0] += 0.5
        #activity discrepancy 
        if(self.impression[2]-self.identity[2]>0):
            #perceived more active increase positivity
            self.emotion[0] += 0.5
        elif(self.impression[2]-self.identity[2]<0):
            #perceived less active decrease positivity
            self.emotion[0] -= 0.5
        #saturate at 4 o -4
        if(self.emotion[0]>=4):
            self.emotion[0]= 4
        elif(self.emotion[0]<= -4):
            self.emotion[0] = -4
        print("emotion: " + str(self.emotion))

    #computation of emotion potency
    def potency(self):
        print("-------- Potency Computation --------")
        #potency impression-identity relate with identity
        sign = int(self.identity[1]/abs(self.identity[1]))
        self.emotion[1] = (self.impression[1] - self.identity[1])*0.5
        #activity-evaluation correlation
        if(self.impression[0]-self.identity[0]>1 and self.identity[2]>1):
            self.emotion[1] += -0.5
        if(self.identity[2]<0 and self.impression[2]>0):
            #inactive perceived active 
            self.emotion[1] += -0.5
        if(self.impression[0]-self.identity[0]>0.5 and self.impression[2]-self.identity[2]<-1):
            self.emotion[1]+= 0.5
        #saturate to max value
        if(self.emotion[0]>=4):
            self.emotion[0]= 4
        elif(self.emotion[0]<= -4):
            self.emotion[0] = -4   
        print("emotion: " + str(self.emotion))

    #computation of emotion activity
    def activity(self):
        print("-------- Activity  Computation --------")
        #check impression - identiy 
        if(self.impression[2]-self.identity[2]>=1):
            #perceived more active
            self.emotion[2] = 2 #high arousal
        elif (self.impression[2]-self.identity[2]>-1):
            #confirmation of activity
            self.emotion[2]= 1 #active/neutral emotion
        else:
            #perceived less active
            self.emotion[2]= -2 #low arousal emotion
        print("emotion: " + str(self.emotion))

    #set user's impression
    def set_impression(self, imp):
        self.impression = imp

    def main(self):
        while(1):
            """
            #input manuale per test senza comunicazione
            data = input("impression in EPA: ").split(',')
            i = []
            for val in data:
                i.append(float(val))
            emoNode.set_impression(i)
            """
            #if identity updated
            if(self.new_imp):
                self.new_imp = False
                print("New impression")
                print(self.impression)
                self.evaluation()
                self.potency()
                self.activity()
                self.new_emo = True
            else:
                #print("No new impression")
                time.sleep(1)

#Emotion Generation Node
emoNode = EmotionGenerator()

#Impression - Emotion connection(pub/sub) 
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

#Emotion Generation-Expression connection (service/client)
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
    