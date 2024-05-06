Emotional Framework
==========

Set up
------
Conda Environments since some nodes run in python3 and the one interacting with Pepper in Python 2.7

### Python 2.7 environment
 * conda create -n py27 python=2.7
 * conda activate py27
 * pip install numpy
 * pip install request
 * pip install flask
 * pip install flask_cors
 * pip install pillow

Working with Pepper having Naoqi 2.5 you need to install it.\
Naoqi installation follow the guidelines on http://doc.aldebaran.com/2-5/dev/python/install_guide.html. \
You can find the SDK release here https://www.aldebaran.com/en/support/pepper-naoqi-2-9/downloads-softwares \
If you encounter any strange problem when try to import naoqi in python due to the sdk being a 32 bit one you can download the Naoqi 2.8 SDK which is a 64bit package https://www.aldebaran.com/en/support/nao-6/downloads-softwares \
You should not face any problem using it from anaconda

### Python 3 environment
* conda create -n emotional-framework python=3.12
* conda activate emotional-framework
* pip install flask
* pip install requests
* pip install python-dotenv
* pip install --upgrade openai

Start 
------
you can use the launch file for windows 
- Avatar Case, use the camera on your laptop, no proximity node, send facial expression cues : stater_avatar.bat
- Pepper Case : starter_pepper.bat It use the camera on Pepper Robot, has the Proximity Perception Module and send the animation to play to the robot. In order to use it correctly make sure to set up the correct IP and Port of your Pepper Robot on the nodes that connect with Pepper and to load the set of emotional animation into the Pepper Robot.  
### Manual Start each Node
Emotion Generation Node
* cd ./Documenti/Tesi/Emotional_Framework/scripts
* conda activate emotional-framework
* python Emotion_Generation.py

Impression Detection Node
* cd ./Documenti/Tesi/Emotional_Framework/scripts
* conda activate emotional-framework
* python Emotion_Generation.py

Morphcast python backend
* cd ./Documents/Morphcast/area42-swat-morphcast/src/backend-python
* conda activate emotional-framework
* python play_backend.py

Emotion and Attention Perception
* cd ./Documenti/Tesi/Emotional_Framework/scripts
* conda activate emotional-framework
* python Emotion_Attention_Perception.py

Emotion Expression
* cd ./Documenti/Tesi/Emotional_Framework/scripts
* conda activate py27
* python Emotion_Expression.py

### For Pepper
PepperVision
* cd ./Documenti/Tesi/Emotional_Framework/scripts
* conda activate py27
* python PepperVision.py

Proximity_Perception
Emotion Expression
* cd ./Documenti/Tesi/Emotional_Framework/scripts
* conda activate py27
* python Proximity_Perception.py

Start Morphcast
http://127.0.0.1:5000/pepper_view

### Avatar/ using computer camera
- open terminal and "conda activate area42-swat-morphcast"
- go into src/sdk-javascript "./Documents/Morphcast/area42-swat-morphcast/src/sdk-javascript"
- run "python -m http.server"
- open your web browser and navigate to http://localhost:8000/play-sdk-v5.html


