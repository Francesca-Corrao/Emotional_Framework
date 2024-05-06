@echo off

start wt -p "Command Prompt" cmd /k "conda activate emotional-framework && cd C:\Users\franc\Documents\Tesi\Emotional_Framework\script && python Emotion_Generation_fixed.py;"
cmd /k "conda activate emotional-framework && cd C:\Users\franc\Documents\Tesi\Emotional_Framework\script && python Impression_Detection.py;"
cmd /k "conda activate emotional-framework && cd C:\Users\franc\Documents\Morphcast\area42-swat-morphcast\src\python-backend && python play_beckend.py;"

cmd /k "conda activate area42-swat-morphcast && cd C:\Users\franc\Documents\Morphcast\area42-swat-morphcast\src\sdk-javascript && python -m http.server;" 
start "" "http://localhost:8000/play-sdk-v5.html"

