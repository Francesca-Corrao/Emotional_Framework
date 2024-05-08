""""
Prendere input audio dal microfono usando pyaudio solo quando è maggiore di una soglia 
"""
import pyaudio
import wave
import time
import os
import struct
import math
import speech_recognition as sr
from flask import Flask, jsonify 

PORT = 6000
rms_threshold = 40
short_normalize = (1.0 / 32768.0)
chunk = 1024
audio_format = pyaudio.paInt16
channels = 1
rate = 44100
s_width = 2
split_silence_time = 1
final_silence_time = 2
recognized_text = " "
data_to_send ={
    "recognized" : False,
    "text": recognized_text
}

def rms(frame):
    count = len(frame) / s_width
    frmt = "%dh" % count
    shorts = struct.unpack(frmt, frame)

    sum_squares = 0.0
    for sample in shorts:
        n = sample * short_normalize
        sum_squares += n * n
    rms = math.pow(sum_squares / count, 0.5)
    return rms * 1000

#creare un oggetto pyAudio
def record():
    print("Starting")
    p = pyaudio.PyAudio()
    #creare un stream audio
    stream = p.open(channels=channels, format= audio_format , input=True, rate = rate, frames_per_buffer= chunk)
    #lista in cui aggiungere input dati dello stream
    listen = []
    start_time = time.time()
    current_time = time.time()
    end_time = time.time() + final_silence_time
    #while -> ascolta fino a un silenzio di 2 secondi
    print("Recording....")
    while(current_time <= end_time):
        #read
        input = stream.read(1024)
        listen.append(input)
        if rms(input) >= rms_threshold:
            end_time = time.time()+final_silence_time
        current_time = time.time()
    print("Recording Done - audio recorder for:",end_time - start_time, "s")
    #stop stream
    stream.start_stream()
    #close stream
    stream.close()
    #terminare pyAudio
    p.terminate()
    #converti lista in byte
    print("Saving in wav file")
    bytecont = b"".join(listen)
    #apriwavfile
    filename = os.path.join(os.getcwd(), 'input_capture.wav')
    wavfile = wave.open(filename, 'wb')
    wavfile.setnchannels(channels)
    wavfile.setsampwidth(p.get_sample_size(audio_format)) 
    wavfile.setframerate(rate)
    #scrivi byte nel wavfil
    wavfile.writeframes(bytecont)
    wavfile.close()


def speech_text():
    #speech recognition
    r = sr.Recognizer()
    filename = "input_capture.wav" 
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        try:
            text = r.recognize_google(audio_data)
            data_to_send["recognized"] = True
            data_to_send["text"]= text
        except sr.UnknownValueError:
            data_to_send["recognized"] = False
            data_to_send[text] = " "

        

"""while(True):
    c = input("Press enter to record: ")
    if(c == ""):
        #record()
        speech_text()
    else:
        print("Wrong character enter:", c,".")
        """

#flask service that record and return the text recognized
app = Flask(__name__)

@app.route('/audio_service', methods = ['GET'])
def audio_service():
    record()
    speech_text()
    print(data_to_send)
    return data_to_send,200

app.run(host='127.0.0.1', port=PORT)