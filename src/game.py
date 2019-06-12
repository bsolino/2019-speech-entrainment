#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 02:48:37 2019

@author: breixo
"""

import os
from nao_utils import create_proxy, IP, PORT
#from word_list_utils import parse_file
from task_utils import read_task_lists

PITCH = 1
SPEED = .75 * 100
LANG = "English"

FILENAME_TASKS = os.path.join("data", "tasks", "selected_tasks.txt")
WORDS_FOLDER = "/home/nao/entrainment/words"



# CONFIGURATION

def configure_voice(tts, language, pitch, speed):
    """
    Prepare the voice to be used by the TTS system

    Default: All at 1. (no modifiers)
    """
    tts.setLanguage(language)
    tts.setParameter("pitchShift", pitch)
    tts.setParameter("speed", speed)
#    tts.setVoice(


# UTILS

def find_word_file(word, words_folder):
    """
    Obtains the route to the word file from the word
    """
    # TODO Improve to be able to select specific frequencies
    return "{}/{}-base.wav".format(words_folder, word) # TODO Adjust 


# ACTIONS

def wait_for_kid(word = ""):
    if word:
        msg = "word: \"{}\"".format(word)
    else:
        msg = "utterance"
    raw_input("Waiting for {}. Press ENTER to continue".format(msg)) # Temporal solution


def say_file(filename, tts, folder):
    word_file = find_word_file(filename, folder)
    print(word_file)
    tts.say("\\audio=\"{}\"\\".format(word_file))


def play_file(filename, aup, folder):
    word_file = find_word_file(filename, folder)
    print(word_file)
    aup.post.playFile(word_file)


# ROBOT UTTERANCES
    
def speak_start_experiment(tts, aup):
    pass #TODO

def speak_before_task(tts, aup, i):
    pass #TODO

def speak_after_task(tts, aup, i):
    pass #TODO
    
def speak_finish_experiment(tts, aup):
    pass #TODO


# TASKS

def execute_task(task, tts, aup, words_folder):
    """
    Plays the game: waits for kind input and then says translation
    """
    for word in task.word_order:
        wait_for_kid(word)
#        say_file(word, tts, words_folder)
        play_file(word, aup, words_folder)


def execute_tasks(list_tasks, tts, aup, words_folder):
    n_tasks = len(list_tasks)
    
    speak_start_experiment(tts, aup)
    
    for i in range(n_tasks):

        
        task = list_tasks[i]
        print("Starting task {}/{}; category: {}".format(
                i+1, n_tasks, task.category))
        raw_input("Press ENTER to continue")

        speak_before_task(tts, aup, i)
        
        execute_task(task, tts, aup, words_folder)
        
        print("Finished task {}/{}".format(i+1, n_tasks))
        
        speak_after_task(tts, aup, i)
    speak_finish_experiment(tts, aup)


def main():
    # Parse properties
    f_tasks = FILENAME_TASKS
    words_folder = WORDS_FOLDER
    ip = IP
    port = PORT
    pitch = PITCH
    speed = SPEED
    language = LANG

    tts = create_proxy("ALTextToSpeech", ip, port)
    configure_voice(tts, language, pitch, speed)
    
    aup = create_proxy("ALAudioPlayer", ip, port)
    
    list_tasks = read_task_lists(f_tasks)
    execute_tasks(list_tasks, tts, aup, words_folder)
    
    


if __name__ == "__main__":
    main()
