import Emotion_Expression as ee
from flask import Flask, request,jsonify
import threading
from naoqi import ALProxy
import json
import time
from datetime import datetime

#pepper ip 
IP_ADD = "10.0.0.2" #set correct IP 
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
    audioplayer = ALProxy("ALAudioPlayer", IP_ADD, PORT)
    sm.setEnabled(True)
    sm.setMode("contextual")
    ts.setLanguage('English')
    ts.setParameter("speed", 80)
    #audio = audioplayer.loadFile("/usr/share/naoqi/wav/random.wav")

@app.route("/talk", methods = ["POST"])
def talk():
    data = request.get_json()
    speech = json.loads(data)
    speech_list = speech.split("_")
    print(datetime.now(), "Requesting Emotion")
    exp.get_emotion()
    time.sleep(1)
    print("Talking")
    for talk in speech_list:
        if type == "R":
            speak.say(str(talk))
        else:
            print(talk)
        time.sleep(1)
    return jsonify(),200
print("Agent Interface")

"""@app.route("/transition", methods = ["POST"])
def transition():
    global audio
    if type == "R":
        audioplayer.play(audio)
    return jsonify(),200"""
threading.Thread(target=exp.main).start()

app.run(host='127.0.0.1', port=PORT2)
