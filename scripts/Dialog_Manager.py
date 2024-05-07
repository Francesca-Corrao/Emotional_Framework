import requests
from dotenv import load_dotenv, find_dotenv
import os
from openai import OpenAI
import time

url = "http://127.0.0.1:3000/" #Emotion-Generation API
_ = load_dotenv(find_dotenv())
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
impression_expected = [0,0,0]
identity = [0,0,0]
emotional_state = [0,0,0]

robot_speech = ""
user_speech = ""
my_messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": ""}
  ]

#request identiy from emotional_framework

while(1):
    #ascolta - requets a Mic Service
    #aggiungere una variabile per dire se la conversazione è iniziata o no 
    #if utente parla rispondi e invia a sentimental analysis
    if(user_speech != ""):
        #send sentimental analysis
        #costruisci messaggio
        my_messages[1]["content"] = user_speech
        #invia a GPT API
        response = client.chat.completions.create(
        model= "gpt-4" ,
        messages=my_messages,
        temperature=1,
        max_tokens=100,)
    #else non risponde -> attira attenzione/aspetta
    
    time.sleep(1)
