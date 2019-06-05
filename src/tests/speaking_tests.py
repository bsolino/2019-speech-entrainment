#!/usr/bin/python
# -*- coding: UTF-8 -*-

#from naoqi import ALProxy
from naoqi import ALBroker, ALModule, ALProxy
from nao_utils import create_proxy, IP, PORT
from time import sleep
from sys import exit
from datetime import datetime
import traceback
import sys

SpeechDetection = None
memory = None


class SpeechDetectionModule(ALModule):
    
    def __init__(self, name):
        ALModule.__init__(self, name)
        
        self.name = name
        
        self.asr = ALProxy("ALSpeechRecognition")
        
        self.tts = ALProxy("ALTextToSpeech")
        
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent(
            "ALSpeechRecognition/Status",
            self.name,
            "onStatusChange")
            
        self.tts.say("Say something to me.")
        
    def onStatusChange(self, arg1, arg2):
        if arg2 == "EndOfProcess":
            print("{}\t{}".format(datetime.now(), arg2))
        
    def subscribeASR(self):
        self.asr.subscribe(self.name)
        
    def unsubscribeASR(self):
        self.asr.unsubscribe(self.name)

def main():
    tts = create_proxy("ALTextToSpeech")

    tts.setLanguage("English")

    my_broker = ALBroker(
        "my_broker",
        "0.0.0.0",      # listen to anyone
        0,              # find a free port and use it
        IP,             # parent broker ip (should be obtained automatically if the module is uploaded)
        PORT)           # parent broker port (should be obtained automatically if the module is uploaded)

    
    asr = create_proxy("ALSpeechRecognition")
    asr.pause(True)
    asr.setLanguage("English")
    asr.setVocabulary(["a"], True)
    
    autmov = create_proxy("ALAutonomousMoves")
    autmov.setExpressiveListeningEnabled(False)

    # Warning: The module must be a global variable
    # The name given to the constructor must be the name of the
    # variable4
    global SpeechDetection
    
    try:
        SpeechDetection = SpeechDetectionModule("SpeechDetection")
        SpeechDetection.subscribeASR()
        asr.pause(False)
        while True:
            sleep(10)
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down")
    except:
        traceback.print_exc()
    
    try:
        SpeechDetection.unsubscribeASR()
    except:
        traceback.print_exc()
    
    asr.pause(True)
    my_broker.shutdown()

    # ~ tts.say("I'm")
    # ~ tts.say("speaking")
    # ~ tts.say("word")
    # ~ tts.say("by")
    # ~ tts.say("word.")

    # ~ tts.say("Het Engelse woord voor vogelbekdier is", "Dutch")
    # ~ tts.say("The English word for platypus is")
#    tts.say("vohel-bekdeer")
#    tts.say("vohelbekdeer")

    sys.exit(0)

if __name__ == "__main__":
    main()