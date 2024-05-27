import requests
import time
import json
from datetime import datetime
url_ic = "http://127.0.0.1:6000/" #Input Capture
url_ai = "http://127.0.0.1:6001/" #agent interface
url_id = "http://127.0.0.1:4000/" #impression detection
output_dic =  {}

select_one = [
    "option one",
    "option 1",
    "one",
    "1",
    "options one",
    "options 1",
]

select_two = [
    "option two",
    "option 2",
    "option to",
    "two",
    "2",
    "to"
    "options two",
    "options 2"
]

def update_dictionary(path):
    global output_dic
    file = open(path)
    data = file.read()
    output_dic = json.loads(data)

def send_choice(key):
    data = json.dumps(output_dic[key]["impression"])
    requests.post(url_id+"choice_impression", json = data)

def main(): 
    print("Dialog Manager : Scripted Story ")
    agent_speech = " "
    user_speech = None
    update_dictionary("C:/Users/franc/Documents/Tesi/Emotional_Framework/Dialog/storia/inizio.txt")
    print(output_dic)
    while(1):
        print("start ", datetime.now())
        #robot_speech
        agent_speech = output_dic['start'] + " How would you like to continue: " + output_dic["option_1"]["continue"] + ", or " + output_dic["option_2"]["continue"] + " ? "
        #post agent_speech
        print("send robot speech")
        data = json.dumps(agent_speech)
        requests.post(url_ai+"/talk", json=data)
        #request user speech
        time.sleep(0.5)
        print("request user_speech")
        while(user_speech == None):
            data = requests.get(url_ic+"/audio_service").json()
            #user_speech = input("insert:")
            if(data['recognized']):
                user_speech = data['text'].lower()
                print(user_speech)
            else:
                user_speech = None
            if user_speech in select_one:
                print("option_1")
                send_choice("option_1")
                update_dictionary(output_dic['option_1']["file"])
            elif user_speech in select_two:
                print("option_2")
                send_choice("option_2")
                update_dictionary(output_dic['option_2']['file'])
            else:
                #no answer get wait for it
                user_speech = None 
                agent_speech = "I am sorry, I didn't get your choice. Can you please try again slowly and louder"
                data = json.dumps(agent_speech)
                requests.post(url_ai+"/talk", json=data)
        user_speech = None
    

main()