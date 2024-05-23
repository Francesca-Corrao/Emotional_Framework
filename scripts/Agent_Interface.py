import Emotion_Expression as ee
from flask import Flask, request,jsonify
import threading
from naoqi import ALProxy
import json
import time

#pepper ip 
IP_ADD = "10.0.0.2" #set correct IP 
PORT = 9559 #set correct PORT 

#REST API PORT
PORT2 = 6001

app = Flask(__name__)
type = "R"
exp = ee.EmotionExpression(type= type)

#pepper speaking Proxy
if type == "R":
    speak = ALProxy("ALAnimatedSpeech", IP_ADD , PORT )
    sm = ALProxy("ALSpeakingMovement", IP_ADD, PORT)
    #speak.setLanguage("English")
    sm.setEnabled(True)
    sm.setMode("contextual")
@app.route("/talk", methods = ["POST"])
def talk():
    data = request.get_json()
    speech = json.loads(data)
    print("Talking")
    exp.get_emotion() #forse meglio mandarla su un thread vediamo
    print(speech)
    if type == "R":
        print(speech)
        speak.say(str(speech))
    #time.sleep(30)
    return jsonify(),200

threading.Thread(target=exp.main).start()

app.run(host='127.0.0.1', port=PORT2)
