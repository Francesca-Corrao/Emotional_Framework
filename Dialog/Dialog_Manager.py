import requests
#from dotenv import load_dotenv, find_dotenv
import os
#from openai import OpenAI
import time
import json

url = "http://127.0.0.1:3000/" #Emotion-Generation API
url_ic = "http://127.0.0.1:6000/" #Input Capture
url_ai = "http://127.0.0.1:6001/"
#_ = load_dotenv(find_dotenv())
#client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
#impression_expected = [0,0,0]
#identity = [0,0,0]
#emotional_state = [0,0,0]
emotional_label = "happy"
conversation_started = False

robot_speech = ""
user_speech = ""
my_messages=[
    {"role": "system", "content": ""},
    {"role": "user", "content": ""}
  ]
#request identiy from emotional_framework
def prompt():
    my_messages[0]["content"] = "You are an artificial social agent interacting with humans."\
    "Your goal is to showcase emotions and make people perceive your identity."\
    "Your identity is friendly. This means you are good, slightly active and potent. "\
    "The emotional state to showcase is " + emotional_label + "The answer must be less then 40 words"
    my_messages[1]["content"] = user_speech

while(1):
    #request user speech
    print("start")
    data = requests.get(url_ic+"/audio_service").json()
    print(data)
    if(data['recognized']):
        user_speech = data['text']
        #send to sentimental analysis / perform sentimental analysis and send it to Emotion interface
        #request emotional state
        print(user_speech)
    else:
        user_speech = ""
    prompt()
    if user_speech != "":
        #user answered respond to him
        robot_speech = "It's great to hear you"
    else:
        #start the conversation
        if(conversation_started):
            #get back his attention
            robot_speech = "Are you still there ?"
        else:
            #start the conversation
            robot_speech = "Nice to see you! I am Pepper"
    #post robot_speech
    print("send robot speech")
    data = json.dump(robot_speech)
    requests.post(url_ai+"/talk", json=data)
    print("done dialog loop")