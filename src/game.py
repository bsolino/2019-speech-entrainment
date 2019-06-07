#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 02:48:37 2019

@author: breixo
"""

import os
from nao_utils import create_proxy, IP, PORT
#from word_list_utils import parse_file
from game_utils import read_task_lists

PITCH = 1
SPEED = .75 * 100
LANG = "English"

FILENAME_TASKS = os.path.join("data", "tasks", "selected_tasks.txt")
FOLDER = "/home/nao/entrainment/words"


def configure_voice(tts, language, pitch, speed):
    """
    Prepare the voice to be used by the TTS system

    Default: All at 1. (no modifiers)
    """
    tts.setLanguage(language)
    tts.setParameter("pitchShift", pitch)
    tts.setParameter("speed", speed)
#    tts.setVoice(


def wait_for_kid(word = ""):
    if word:
        msg = "word: \"{}\"".format(word)
    else:
        msg = "utterance"
    raw_input("Waiting for {}. Press ENTER to continue".format(msg)) # Temporal solution
    
    
def find_word_file(word, folder):
    """
    Obtains the route to the word file from the word
    """
    # TODO Improve to be able to select specific frequencies
    return "{}/{}-base.wav".format(folder, word) # TODO Adjust 


def say_word(word, tts, folder):
    word_file = find_word_file(word, folder)
    print(word_file)
    tts.say("\\audio=\"{}\"\\".format(word_file))
    #aup = create_proxy("ALAudioPlayer")
    #aup.post.playFile("/usr/share/naoqi/wav/filename.wav")


def execute_task(task, tts, folder):
    """
    Plays the game: waits for kind input and then says translation
    """
    for word in task.word_order:
        wait_for_kid(word)
        say_word(word, tts, folder)


def execute_tasks(list_tasks, tts, folder):
    n_tasks = len(list_tasks)
    for i in range(n_tasks):

        task = list_tasks[i]
        print("Starting task {}/{}; category: {}".format(
                i+1, n_tasks, task.category))
        raw_input("Press ENTER to continue")
        
        execute_task(task, tts, folder)
        
        print("Finished task {}/{}".format(i+1, n_tasks))

def main():
    # Parse properties
    f_tasks = FILENAME_TASKS
    folder = FOLDER
    ip = IP
    port = PORT
    pitch = PITCH
    speed = SPEED
    language = LANG

    tts = create_proxy("ALTextToSpeech", ip, port)
    configure_voice(tts, language, pitch, speed)
    
    list_tasks = read_task_lists(f_tasks)
    execute_tasks(list_tasks, tts, folder)
    
    


if __name__ == "__main__":
    main()
