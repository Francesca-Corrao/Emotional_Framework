import time
import requests

url2 = 'http://127.0.0.1:4000' #impression_detection
output_data = {}

def update_data():
    output_data["id"] = int(input("ID:"))
    output_data["dist"] = float(input("DIST:"))
    output_data["gaze"] = int(input("gaze:"))
    output_data["gaze_level"] = float(input("Gaze_level:"))

while(1):
    update_data()
    print(output_data)
    #data2 = json.dumps(dist)
    requests.post(url2+"/gaze_prox_perception", json=output_data)
    time.sleep(3)
