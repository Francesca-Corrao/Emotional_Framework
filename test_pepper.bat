@echo off

start wt -p "Command Prompt" cmd /k "title Emotion_Generator && conda activate emotional-framework && cd C:/Users/franc/Documents/Tesi/Emotional_Framework/scripts && python Emotion_Generation_fixed.py;" cmd /k "title Impression_Detection && conda activate emotional-framework && cd C:/Users/franc/Documents/Tesi/Emotional_Framework/Dialog && python Impression_Detection_Story.py;" cmd /k "title Input_Capture && conda activate emotional-framework && cd C:/Users/franc/Documents/Tesi/Emotional_Framework/Dialog && python Input_capture.py;" cmd /k "conda activate emotional-framework && cd C:/Users/franc/Documents/Morphcast/area42-swat-morphcast/src/backend-python && python play_backend.py;" cmd /k "conda activate emotional-framework && cd C:/Users/franc/Documents/Tesi/Emotional_Framework/scripts && python Emotion_Attention_Perception.py;" cmd /k "title Agent_Interface && conda activate py27 && cd C:/Users/franc/Documents/Tesi/Emotional_Framework/scripts && python Agent_Interface.py;" cmd /k "conda activate py27 && cd C:/Users/franc/Documents/Tesi/Emotional_Framework/scripts && python PepperVision.py;" cmd /k "conda activate py27 && cd C:/Users/franc/Documents/Tesi/Emotional_Framework/scripts && python Gaze_Perception.py;" cmd /k "title Dialog Manager && conda activate emotional-framework && cd C:/Users/franc/Documents/Tesi/Emotional_Framework/Dialog && python Scripted_Story.py;"


