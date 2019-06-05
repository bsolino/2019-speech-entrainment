#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

from naoqi import ALProxy

IP = "192.168.0.199"
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
    posture = create_proxy("ALRobotPosture")
    motion.setBreathEnabled("Body", False)
    posture.goToPosture("Crouch", 0.5)

def regain_connection():
    mem = create_proxy("ALMemory")
    