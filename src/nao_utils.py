#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

from naoqi import ALProxy

IP_WIFI = "192.168.0.199"
IP_CABLE = "192.168.0.197"

#IP = IP_WIFI
IP = IP_CABLE

PORT = 9559

def create_proxy(proxy_name, ip = IP, port = PORT):
    """
    Creates a proxy by given name.
    Some names are:
    * "ALSpeechRecognition"     Speech recognition
    * "ALTextToSpeech"          Text to speech
    * "ALAutonomousLife"        Controls robot life
    * "ALRobotPosture"          Controls robot posture
    """
    return ALProxy(proxy_name, ip, port)
    
def crouch():
    motion = create_proxy("ALMotion")
    motion.setBreathEnabled("Body", False)
    posture = create_proxy("ALRobotPosture")
    posture.goToPosture("Crouch", 0.5)
    #TODO This makes the robot hot --> turn off motors?
    

def regain_connection():
    mem = create_proxy("ALMemory")
    
