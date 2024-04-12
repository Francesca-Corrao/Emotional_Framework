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

#rest API
app = Flask(__name__)


#define class
class EmotionGenerator:
    def __init__(self) -> None:
        self.identity = [1,1,1] #identity in EPA space
        self.impression = [0,0,0] #impression in EPA space
        self.emotion = [0,0,0] #emotion in EPA space
        self.new_imp = False
        self.new_emo = False
        #subscriber a /impression
        #service /emotion_service

    #computation of emotion evaluation
    """def evaluation(self):
        print("-------- Evaluation Computation --------")
        #check impression evaluation
        if(self.impression[0]>=0):
        #look good -> good emotions
            self.emotion[0]= 1.5
            if(self.identity[0]<2):
                #modest positive identity -> higher positivity
                self.emotion[0] += 1
            if(self.identity[2]<=0):
                #quiet individual greater higher emotions
                self.emotion[0] += 0.5
        else:
        #look bad -> bad emotion
            self.emotion[0]= -1
            if(self.identity[0]>1):
                #high evaluation -> higher negativity
                self.emotion[0] += -1.0

        #check activity discrepancy
       if(self.impression[2]-self.identity[2]>0):
            #perceived more active increase positivity
            self.emotion[0] += 0.5
        elif(self.impression[2]-self.identity[2]<0):
            #perceived less active decrease positivity
            self.emotion[0] -= 0.5
        print("emotion: " + str(self.emotion))
    """

    def evaluation(self):
        print("-------- Evaluation Computation --------")
    
        #positivity varies directly with valence of impression
        sign = int(self.impression[0]/abs(self.impression[0]))
        #intensity varies with identity evaluation
        val = abs(-self.identity[0]+self.impression[0]+sign*1)
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
        """if(self.impression[1]-self.identity[1]>=1):
            #more power
            self.emotion[1]= 1.0
            if(self.identity[1]<-1):
            #identy powerless -> higher power
                self.emotion[1]+= 1 

        elif(self.impression[1]-self.identity[1]>-1):
            #match power
            self.emotion[1] += 0.5
        else:
            #less power
            self.emotion[1] = -1.0
            if(self.identity[1]>1 and self.identity[0]>1):
                #indentity powerfull -> less powerfull (?)
                self.emotion[1] += -1
        """
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

    #set/get user's impression
    def set_impression(self, imp):
        self.impression = imp

    def main(self):
        while(1):
        #get identity
            """data = input("impression in EPA: ").split(',')
            i = []
            for val in data:
                i.append(float(val))
            emoNode.set_impression(i)
            """
            if(self.new_imp):
                self.new_imp = False
                print("New impression")
                print(self.impression)
                self.evaluation()
                self.potency()
                self.activity()
                self.new_emo = True
            #else:
                #print("No new impression")
                #time.sleep(1)

emoNode = EmotionGenerator()

#rest API
@app.route('/impression',methods =['POST'])
def get_impression():
    #receive impression from Impression Node
    print("Received Impression")
    #convert fro json to array
    data = request.get_json()
    i = json.loads(data)
    emoNode.new_imp = True
    emoNode.set_impression(i)

    #i = data
    #emoNode.set_impression(i)
    return jsonify({'succes':'True'}),200

@app.route('/emotional_state',methods =['GET'])
def send_emotion():
    print("Received Request from Emotional expression")
    val = emoNode.new_emo
    emoNode.new_emo = False
    return jsonify({'new_emotion': val, 'emotion':emoNode.emotion}),200

if __name__ == '__main__':
    threading.Thread(target=emoNode.main).start()
    app.run(host='127.0.0.1', port=3000)
    