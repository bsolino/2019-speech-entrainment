#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 02:48:37 2019

@author: breixo
"""

from nao_utils import create_proxy, IP, PORT
from word_list_utils import parse_file

PITCH = 1
SPEED = 1
LANG = "English"

FILENAME = "list_words.txt"
FOLDER = "words"


def configure_voice(tts, language, pitch, speed):
    """
    Prepare the voice to be used by the TTS system

    Default: All at 1. (no modifiers)
    """
    tts.setLanguage(language)
    tts.setParameter("pitchShift", pitch)
    tts.setParameter("speed", speed)
#    tts.setVoice(



def main():
    # Parse properties
    filename = FILENAME
    folder = FOLDER
    ip = IP
    port = PORT
    pitch = PITCH
    speed = SPEED
    language = LANG

    tts = create_proxy("ALTextToSpeech", ip, port)
    configure_voice(tts, language, pitch, speed)
    
    experiment_words = parse_file(filename)
    


if __name__ == "__main__":
    main()
