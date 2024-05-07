""""
Prendere input audio dal microfono usando pyaudio solo quando è maggiore di una soglia 
"""
import pyaudio
import wave
import time
import os
import struct
import math

rms_threshold = 40
short_normalize = (1.0 / 32768.0)
chunk = 1024
audio_format = pyaudio.paInt16
channels = 1
rate = 44100
s_width = 2
split_silence_time = 1
final_silence_time = 2

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
    wavfile.writeframes(bytecont)
    wavfile.close()
    print("DONE")
    #scrivi byte nel wavfil

while(True):
    c = input("Press enter to record: ")
    if(c == ""):
        record()
    else:
        print("Wrong character enter:", c,".")