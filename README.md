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
* conda create -n emotional-framework
* conda activate emotional-framework
* pip install flask
* pip install requests
* pip install threading

Node
------