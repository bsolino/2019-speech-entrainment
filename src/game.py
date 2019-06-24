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
from time import sleep

FILENAME_TASKS = os.path.join("data", "tasks", "selected_tasks.txt")
NAO_FOLDER = "/home/nao/entrainment"
WORDS_FOLDER = NAO_FOLDER + "/words"
INTERACTIONS_FOLDER = NAO_FOLDER + "/interactions_s100_p1.15"



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


def play_file(filename, aup, folder):
    word_file = find_word_file(filename, folder)
    print(word_file)
    aup.post.playFile(word_file)


# ROBOT UTTERANCES

def execute_interaction(script, aup, folder, start_point = 0):
    i = start_point
    for action in script:
        if type(action) is int:
            n_sentences = action
            i += 1
            for i in range(i, i + n_sentences):
                aup.playFile(folder + "/{:0>2d}-base.wav".format(i))
        elif action == "wait":
            wait_for_kid()
        elif action == "pause":
            sleep(1)  # TODO? Add variation?


def find_start_interaction(scripts, n_interaction):
    start_point = 0
    for i in range(n_interaction):
        for action in scripts[i]:
            if type(action) is int:
                start_point += action
    return start_point


def speak_start_experiment(aup):
    folder = INTERACTIONS_FOLDER + "/base/start_experiment"
    script = [2, "wait", 3, "wait", 1, "pause", 3, "pause", 1, "wait", 1]
    execute_interaction(script, aup, folder)


def speak_before_task(aup, n_interaction):
    folder = INTERACTIONS_FOLDER + "/base/before_task"
    scripts = [
            [2],
            [2, "pause", 1, "wait", 1],
            [2, "pause", 1, "wait", 2],
            [2, "pause", 1, "wait", 1]
            ]
    start_point = find_start_interaction(scripts, n_interaction)
    script = scripts[n_interaction]
    execute_interaction(script, aup, folder, start_point)


def speak_after_task(aup, n_interaction):
    folder = INTERACTIONS_FOLDER + "/base/after_task"
    scripts = [[1], [1], [1], [1]]
    start_point = find_start_interaction(scripts, n_interaction)
    script = scripts[n_interaction]
    execute_interaction(script, aup, folder, start_point)


def speak_finish_experiment(aup):
    folder = INTERACTIONS_FOLDER + "/base/finish_experiment"
    script = [2, "wait", 3]
    execute_interaction(script, aup, folder)


# TASKS

def execute_task(task, aup, words_folder):
    """
    Plays the game: waits for kind input and then says translation
    """
    for word in task.word_order:
        wait_for_kid(word)
        play_file(word, aup, words_folder)


def execute_tasks(list_tasks, aup, words_folder):
    n_tasks = len(list_tasks)
    
    speak_start_experiment(aup)
    
    for i in range(n_tasks):

        
        task = list_tasks[i]
        print("Starting task {}/{}; category: {}".format(
                i+1, n_tasks, task.category))
        raw_input("Press ENTER to continue")

        speak_before_task(aup, i)
        
        execute_task(task, aup, words_folder)
        
        print("Finished task {}/{}".format(i+1, n_tasks))
        raw_input("Press ENTER to finish task")
        speak_after_task(aup, i)
    speak_finish_experiment(aup)


def main():
    # Parse properties
    f_tasks = FILENAME_TASKS
    words_folder = WORDS_FOLDER
    interactions_folder = INTERACTIONS_FOLDER
    ip = IP
    port = PORT

    aup = create_proxy("ALAudioPlayer", ip, port)
    
    
    list_tasks = read_task_lists(f_tasks)
    execute_tasks(list_tasks, aup, words_folder)
    
    


if __name__ == "__main__":
    main()
