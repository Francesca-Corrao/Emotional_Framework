"""
Node that manages the interaction between the robot and the human.
- Send to the robot the speech it has to say
- Get the choice of the user, either by keyboard or using the microphone
- Continue the story according to the choice and send the impression associated to the choice to the impression detection node  
"""

import requests
import time
import json
from datetime import datetime
url_ic = "http://127.0.0.1:6000/" #Input Capture API
url_ai = "http://127.0.0.1:6001/" #Agent Interface API
url_id = "http://127.0.0.1:4000/" #Impression Detection API
output_dic =  {}
end_point=False
select_one = [
    "option one",
    "option 1",
    "one",
    "1",
    "options one",
    "options 1"
]

select_two = [
    "option two",
    "option 2",
    "two",
    "2",
    "options two",
    "options 2"
]

def update_dictionary(path):
    #Function to update the paragraph of the story to tell
    global output_dic, end_point
    file = open(path)
    data = file.read()
    output_dic = json.loads(data)
    if "finish.txt" in path:
        end_point = True

def send_choice(key):
    #Function to send the impression associated with the choice to the Impression Detection Node
    data = json.dumps(output_dic[key]["impression"])
    requests.post(url_id+"choice_impression", json = data)

def main(): 
    global end_point
    print("Dialog Manager : Scripted Story ")
    agent_speech = " "
    user_speech = None
    update_dictionary("C:/Users/franc/Documents/Tesi/Emotional_Framework/Dialog/storia_fantasy/begin.txt")
    
    start = True
    first_state = "H"
    time.sleep(11) #wait for other nodes to start--- connection to Pepper takes time
    while(1):
        print("start ", datetime.now())
        #robot_speech
        agent_speech = output_dic['start']
        if output_dic["option_1"]["continue"] != " " : 
            agent_speech += "_Cosa vuoi fare: " + output_dic["option_1"]["continue"] + ", o " + output_dic["option_2"]["continue"] + " ? "
            #post agent_speech
            print("send robot speech")
            data = json.dumps(agent_speech)
            requests.post(url_ai+"/talk", json=data)
            #request user speech
            time.sleep(0.5)
            print("request user_speech")
            while(user_speech == None):
                user_speech = input("insert:")
                """
                data = requests.get(url_ic+"/audio_service").json()
                if(data['recognized']):
                    user_speech = data['text'].lower()
                    print(user_speech)
                else:
                    user_speech = None"""
                if user_speech in select_one:
                    if(start):
                        start = False
                        first_state = "SA"
                    print("option_1")
                    send_choice("option_1")
                    if(output_dic["option_1"]["to_say"] != ""):
                        time.sleep(1)
                        data = json.dumps(output_dic["option_1"]["to_say"])
                        requests.post(url_ai+"/talk", json=data)
                    update_dictionary(output_dic['option_1']["file"])
                elif user_speech in select_two:
                    if(start):
                        start = False
                        first_state = "H"
                    print("option_2")
                    send_choice("option_2")
                    if(output_dic["option_2"]["to_say"] != ""):
                        time.sleep(1)
                        data = json.dumps(output_dic["option_2"]["to_say"])
                        requests.post(url_ai+"/talk", json=data)
                    update_dictionary(output_dic['option_2']['file'])
                else:
                    #no answer get wait for it
                    user_speech = None 
                    agent_speech = "Mi dispiace non ho capito che hai detto, puoi ripetere ?"
                    data = json.dumps(agent_speech)
                    requests.post(url_ai+"/talk", json=data)
            user_speech = None
            time.sleep(2)
        else:
            data = json.dumps(agent_speech)
            requests.post(url_ai+"/talk", json=data)
            time.sleep(2)
            if end_point:
                if first_state == "SA":
                    #end happy
                    send_choice("option_1")
                else:
                    #end sad
                    send_choice("option_2")
            else:
                send_choice("option_1")
            if(output_dic["option_1"]["to_say"] != ""):
                    data = json.dumps(output_dic["option_1"]["to_say"])
                    requests.post(url_ai+"/talk", json=data)
            if end_point:
                print("End Story")
                break
            update_dictionary(output_dic['option_1']['file'])
            
            #time.sleep(5)
            

main()