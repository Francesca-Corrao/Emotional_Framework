import Emotion_Expression as ee
from flask import Flask, request,jsonify
import threading
from naoqi import ALProxy, qi
import json
import time
from datetime import datetime

#pepper ip 
IP_ADD = "10.0.0.6" #set correct IP 
PORT = 9559 #set correct PORT 

#REST API PORT
PORT2 = 6001

app = Flask(__name__)
type = "R"
exp = ee.EmotionExpression(type= type)
audio = None
#pepper speaking Proxy
if type == "R":
    speak = ALProxy("ALAnimatedSpeech", IP_ADD , PORT )
    sm = ALProxy("ALSpeakingMovement", IP_ADD, PORT)
    ts = ALProxy("ALTextToSpeech", IP_ADD,PORT)
    bm = ALProxy("ALBehaviorManager", IP_ADD, PORT)
    sm.setEnabled(True)
    sm.setMode("contextual")
    ts.setLanguage('English')
    ts.setParameter("speed", 80)
    bm.preloadBehavior("my_sounds/play_clock")

@app.route("/talk", methods = ["POST"])
def talk():
    data = request.get_json()
    speech = json.loads(data)
    speech_list = speech.split("_")
    exp.get_emotion()
    #time.sleep(1)
    print("Talking")
    for talk in speech_list:
        print(talk)
        if talk == "^":
            #play sound
            bm.runBehavior("my_sounds/play_clock")
        else:
            #exp.get_emotion()
            if type == "R":
                speak.say(str(talk))
            else:
                print(talk)
            time.sleep(1.5)

    return jsonify(),200
print("Agent Interface")


threading.Thread(target=exp.main).start()

app.run(host='127.0.0.1', port=PORT2)
