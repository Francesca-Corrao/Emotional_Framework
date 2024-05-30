from naoqi import ALProxy
#Pepper Connection
IP_ADD = "10.0.0.2" #set correct IP 
PORT = 9559 #set correct PORT 
behaviour_player = ALProxy("ALBehaviorManager", IP_ADD , PORT )
animation_player = ALProxy("ALAnimationPlayer", IP_ADD, PORT)
animation = 'emotions-8fe336/Happy_2'
#behaviour_player.runBehavior(animation)
animation_player.run(animation)
print("done")