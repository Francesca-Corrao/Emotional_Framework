import Emotion_Expression
from flask import Flask
import threading

PORT = 6001
app = Flask(__name__)

exp = Emotion_Expression(type= "R")

#pepper speaking Proxy

@app.route("/talk", methods = ["POST"])
def talk():
    print("Talking")

@app.route("/get_emotion", methods = ["GET"])
def return_emotion():
    emo = exp.emo_label
    emo_string = ""
    if emo == "H":
        emo_string = "happy"
    elif emo == "A":
        emo_string = "angry"
    elif emo == "SA":
        emo_string = "sad"
    elif emo == "SU":
        emo_string = "surprise"
    elif emo == "F":
        emo_string = "fear"
    elif emo == "D":
        emo_string = "disgust"
    else:
        emo_string = "neutral"

    return emo_string, 200

threading.Thread(target=exp.main).start()

app.run(host='127.0.0.1', port=PORT)
