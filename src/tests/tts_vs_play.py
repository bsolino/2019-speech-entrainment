#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 18:22:35 2019

@author: breixo
"""

from nao_utils import create_proxy, IP, PORT
#from word_list_utils import parse_file
from game_utils import read_task_lists
from game import say_file, play_file, configure_voice, wait_for_kid, PITCH, SPEED, LANG, FILENAME_TASKS, WORDS_FOLDER
from datetime import datetime




    
    
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
    
    i = 0
    task = list_tasks[i]
    print("Starting task {}; category: {}".format(
            i+1, task.category))
    raw_input("Press ENTER to continue")
    
    for word in task:
        wait_for_kid(word)
        raw_input("Press ENTER to Test TextToSpeech")
        start = datetime.now().microsecond
        say_file(word, tts, words_folder)
        end = datetime.now().microsecond
        print("It took {} miliseconds".format((end - start)))
        
        raw_input("Press ENTER to Test AudioPlayer")
        start = datetime.now().microsecond
        play_file(word, aup, words_folder)
        end = datetime.now().microsecond
        print("It took {} miliseconds".format((end - start)))
    
    


if __name__ == "__main__":
    main()
