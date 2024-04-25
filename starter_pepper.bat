@echo off

start wt -p "Command Prompt" cmd /k "conda activate emotional-framework && cd C:\Users\franc\Documents\Tesi\Emotional_Framework\script && python Emotion_Generation_fixed.py;"
cmd /k "conda activate emotional-framework && cd C:\Users\franc\Documents\Tesi\Emotional_Framework\script && python Impression_Detection.py;"
cmd /k "conda activate emotional-framework && cd C:\Users\franc\Documents\Morphcast\area42-swat-morphcast\src\backend-python && play_backend.py;"
cmd /k "conda activate emotional-framework && cd C:\Users\franc\Documents\Tesi\Emotional_Framework\script && python Emotion_Attention_Perception.py;"
cmd /k "conda activate py27 && cd C:\Users\franc\Documents\Tesi\Emotional_Framework\script && python Emotion_Expression.py;"
cmd /k "conda activate py27 && cd C:\Users\franc\Documents\Tesi\Emotional_Framework\script && python PepperVision.py;"
cmd /k "conda activate py27 && cd C:\Users\franc\Documents\Tesi\Emotional_Framework\script && python Proximity_Perception.py"
start "" "http://localhost:5000/morphcast.html"

