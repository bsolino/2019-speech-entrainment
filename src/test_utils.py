#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 22:23:14 2019

@author: breixo
"""

class AudioPlayerMock:
    class post:
        @staticmethod
        def playFile(path):
            print("Non blocking. File: {}".format(path))
    
    @staticmethod
    def playFile(path):
        print("Blocking. File: {}".format(path))

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
