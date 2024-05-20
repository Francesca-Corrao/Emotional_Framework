import requests
#from dotenv import load_dotenv, find_dotenv
import os
#from openai import OpenAI
import time
import json

url_ic = "http://127.0.0.1:6000/" #Input Capture
url_ai = "http://127.0.0.1:6001/"

def update_dictionary(path):
    global output_dic
    file = open(path)
    data = file.read()
    output_dic = json.loads(data)
    print(output_dic)

agent_speech = " "
user_speech = None
output_dic =  {}
update_dictionary("./storia/inizio.txt")
print(type(output_dic))
while(1):
    print("start")
    #robot_speech
    agent_speech = output_dic['start'] + " How would you like to continue: " + output_dic["option_1"] + " or " + output_dic["option_2"] + " ? "
    #post agent_speech
    print("send robot speech")
    data = json.dumps(agent_speech)
    #requests.post(url_ai+"/talk", json=data)
    #request user speech
    print("request user_speech")
    while(user_speech == None):
        #data = requests.get(url_ic+"/audio_service").json()
        user_speech = input("insert:")
        print(data)
        """if(data['recognized']):
            user_speech = data['text']
            #send to sentimental analysis / perform sentimental analysis and send it to Emotion interface
            #request emotional state
            print(user_speech)
        else:
            user_speech = None
        """
            
        if user_speech == "option one":
            print("option_1")
            update_dictionary(output_dic['option_1_file'])

        elif user_speech == "option two":
            print("option_2")
            update_dictionary(output_dic['option_2_file'])
        else:
            #no answer get wait for it
            user_speech = None 
            agent_speech = "I am sorry I didn't get your choice. Can you please try againg slowly and louder"
            data = json.dumps(agent_speech)
            requests.post(url_ai+"/talk", json=data)
    user_speech = None
    print("done dialog loop")