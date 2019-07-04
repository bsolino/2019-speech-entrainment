#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 22:23:14 2019

@author: breixo
"""

from game_constants import NAO_FOLDER
from audio_utils import play_file
from os.path import pardir, join

AUDIO = True

class AudioPlayerMock:
    
    class post:
        @staticmethod
        def playFile(path):
            print("Non blocking. File: {}".format(path))
            if AUDIO:
                play_file(AudioPlayerMock.adapt_path(path))
    
    @staticmethod
    def playFile(path):
        print("Blocking. File: {}".format(path))
        if AUDIO:
            play_file(AudioPlayerMock.adapt_path(path))
    
    @staticmethod
    def adapt_path(path):
        new_path = path.replace(NAO_FOLDER, "").split("/")
        return join(pardir, "resources", "adapted", *new_path)

class TextToSpeechMock:
    @staticmethod
    def say(_str):
        print("Say: {}".format(_str))
    
    @staticmethod
    def sayToFile(_str, _file):
        print("Say: \"{}\" to file: {}".format(_str, _file))

    @staticmethod
    def setLanguage(language):
        print("Language = {}".format(language))
    
    @staticmethod
    def setParameter(parameter, value):
        print("Set parameter {} to value {}".format(parameter, value))
        
class BehaviorManagerMock:
    @staticmethod
    def startBehavior(route):
        print("BehaviorManagerMock: startBehavior(\"{}\")".format(route))

class MotionMock:
    @staticmethod
    def wakeUp():
        print("MotionMock: wakeUp()")
        
    @staticmethod
    def rest():
        print("MotionMock: rest()")
    
    @staticmethod    
    def setBreathEnabled(robot_part, enabled):
        print("MotionMock: setBreathEnabled({}, {})".format(
                robot_part, enabled))