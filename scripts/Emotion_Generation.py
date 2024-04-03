""" Emotion Generation Component: take as input the impressione the human has of the agent 
and produce the emotion the robot should feel according to the Affect Control Theory.
Three main components, each computing one of the value of the emotion in the EPA space:
-Evaluation 
-Potency 
-Activity
"""

#import needed

#define class
class EmotionGenerator:
    def __init__(self) -> None:
        self.identity = [0,0,0] #identity in EPA space
        self.impression = [0,0,0] #impression in EPA space
        self.emotion = [0,0,0] #emotion in EPA space
        #subscriber a /impression
        #service /emotion_service

    #computation of emotion evaluation
    def evaluation(self):
        #check impression evaluation
        if(self.impression[0]>=0):
        #look good -> good emotions
            self.emotion[0]= 1
            if(self.identity[0]<2):
                #modest positive identity -> higher positivity
                self.emotion[0] += 1
            if(self.impression[2]<=0):
                #quiet individual greater higher emotions
                self.emotion[0] += 0.5

        else:
        #look bad -> bad emotion
            self.emotion[0]= -1
            if(self.identity[0]>1):
                #high evaluation -> higher negativity
                self.emotion[0] += -1.0

        #check activity discrepancy
        if(self.identity[2]-self.identity[2]>0):
            #perceived more active increase positivity
            self.emotion += 0.5
        elif(self.identity[2]-self.identity[2]<0):
            #perceived less active decrease positivity
            self.emotion -= 0.5
        print("evaluation: " + self.emotion[0])

    #computation of emotion potency
    def potency(self):
        #potency impression-identity relate with identity
        if(self.impression[1]-self.identity[1]>=1):
            #more power
            self.emotion[1]= 1.0
            if(self.identity[1]<-1):
            #identy powerless -> higher power
                self.emotion[1]+= 1 

        elif(self.impression[1]-self.identity[1]>-1):
            #match power
            self.emotion[0] = 1.0
        else:
            #less powe
            self.emotion[1] = -1.0
            if(self.identity[1]>1 and self.identity[0]>1):
                #indentity powerfull -> less powerfull (?)
                self.emotion[1] += -1

        #activity-evaluation correlation
        if(self.impression[0]-self.identity[0]>1 and self.identity[2]>1):
            self.emotion[1] += -0.5
               
        print(self.emotion[1])

    #computation of emotion activity
    def activity(self):
        #check impression - identiy 
        if(self.impression[2]-self.identity[2]>=1):
            #perceived more active
            self.emotion[2] = 2 #high arousal
            self.emotion[1] += -0.5 #lower potency emotion
        elif (self.impression[2]-self.identity[2]>-1):
            #confirmation of activity
            self.emotion[2]= 1 #active/neutral emotion
        else:
            #perceived less active
            self.emotion[2]= -2 #low arousal emotion
            self.emotion[1] += 1 #high potency empotion
        print(self.emotion[2])

    #set/get user's impression
    def set_impression(self, imp):
        self.impression = imp
   
#main
def main():
    emoNode = EmotionGenerator()
    while(1):
        #get identity
        emoNode.evaluation()
        emoNode.potency()
        emoNode.activity()


if __name__ == '__main__':
    main()