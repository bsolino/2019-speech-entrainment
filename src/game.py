#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 02:48:37 2019

@author: breixo
"""

from os import listdir, makedirs
from os.path import join, abspath, exists
from shutil import rmtree
from nao_utils import create_proxy, IP, PORT
#from word_list_utils import parse_file
from task_utils import read_task_lists
from audio_utils import record_manual, record_to_file
from time import sleep
from praat_utils import extract_features, parse_mean_pitch
from distutils.util import strtobool

# Local data
from game_constants import FILENAME_TASKS, PARTICIPANTS_DATA_FOLDER
# NAO Data
from game_constants import NAO_FOLDER, WORDS_FOLDER_TEMPLATE, INTERACTIONS_FOLDER_TEMPLATE
#from game_constants import  WORDS_NELLEKE, WORDS_JUDITH
# Voice Data
from game_constants import PITCH_WORDS, SPEED_WORDS, PITCH_INTERACTIONS, SPEED_INTERACTIONS
# Entrainment
from game_constants import MIN_PITCH, MAX_PITCH, ROUND_STEP
# Interaction scripts
from game_constants import SCRIPT_START, SCRIPT_BEFORE_TASK, SCRIPT_AFTER_ITEM, SCRIPT_AFTER_TASK, SCRIPT_FINISH 

from test_utils import AudioPlayerMock, BehaviorManagerMock

WORDS_FOLDER = NAO_FOLDER + WORDS_FOLDER_TEMPLATE.format(
        SPEED_WORDS, PITCH_WORDS)
#WORDS_FOLDER = NAO_FOLDER + WORDS_NELLEKE
#WORDS_FOLDER = NAO_FOLDER + WORDS_JUDITH
INTERACTIONS_FOLDER = NAO_FOLDER + INTERACTIONS_FOLDER_TEMPLATE.format(
        SPEED_INTERACTIONS, PITCH_INTERACTIONS)

UNKNOWN_WORDS = ["ear", "walk"]

#CONSTANTS
DEBUG = True

# CONFIGURATION GLOBAL VARIABLES
participant_id = None
entrainment = None
p_folder = None

be_mngr = None


"""
Hacks to Silence PyAudio warnings
"""

import sys
sys.stderr = open(join("return","logfile.txt"), 'ab')


# UTILS

def find_word_file(word, words_folder, target_pitch):
    """
    Obtains the route to the word file from the word
    """
    if not entrainment:
       target_pitch = "base"
    return "{}/{}-{}.wav".format(words_folder, word, target_pitch)
    



def input_boolean(msg, default = False):
    a_boolean = None
    while a_boolean is None:
        _input = raw_input(msg)
        if _input:
            try:
                a_boolean = strtobool(_input)
            except ValueError:
                print("ERROR: {} is not a valid value.".format(_input))
        else:
            a_boolean = default
    return a_boolean


def analyze_audio_data(base_path, audio_data, sample_width):
    audio_file = base_path + ".wav"
    features_file = base_path + ".txt"
    record_to_file(audio_file, audio_data, sample_width)
    extract_features(audio_file, features_file)
    return parse_mean_pitch(features_file)


def round_and_bound_pitch(x):
    base = ROUND_STEP
    value = int(base * round(float(x)/base))
    ret = max(MIN_PITCH, min(MAX_PITCH, value))
    print("Original value = {}; Rounded = {}; returns = {}".format(x, value, ret))
    return ret

# ACTIONS

def wait_for_kid(word = "", base_path = "", msg = ""):
    if msg == "":
        if word:
            msg_word = "word: \"{}\"".format(word)
        else:
            msg_word = "utterance"
        msg = "Waiting for {}. Press ENTER to continue".format(msg_word)
    target_pitch = None
    if base_path:
        sample_width, audio_data = record_manual()
        mean_pitch = analyze_audio_data(base_path, audio_data, sample_width)
        if mean_pitch:
            target_pitch = round_and_bound_pitch(mean_pitch)
    raw_input(msg) # Temporal solution
    return target_pitch


def play_file(filename, target_freq, folder, aup):
    word_file = find_word_file(filename, folder, target_freq)
    print(word_file)
    aup.post.playFile(word_file)
#    aup.playFile(word_file) # Testing blocking the call


# ROBOT UTTERANCES

def execute_interaction(script, aup, folder, start_point = 0):
    i = start_point
    for action in script:
        if type(action) is int:
            n_sentences = action
            i_last_sentence = i + n_sentences
            i += 1
            for i in range(i, i_last_sentence+1):
                audio_file = folder + "/{:0>2d}-base.wav".format(i)
                print("Interaction {} of {}".format(i, i_last_sentence))
                aup.playFile(audio_file)
                if i < i_last_sentence:
                    print("Pausing")
                    sleep(0.7)
        elif action == "wait":
            wait_for_kid()
        elif action == "pause":
            sleep(0.7)  # TODO? Add variation?
        else:
            # We assume that it'll be an animation address
            global be_mngr
        
            be_mngr.startBehavior(action)


def find_start_interaction(scripts, n_interaction):
    start_point = 0
    for i in range(n_interaction):
        for action in scripts[i]:
            if type(action) is int:
                start_point += action
    return start_point


def speak_start_experiment(aup):
    folder = INTERACTIONS_FOLDER + "/start_experiment"
    script = SCRIPT_START
    execute_interaction(script, aup, folder)


def speak_before_task(aup, n_interaction):
    folder = INTERACTIONS_FOLDER + "/before_task"
    scripts = SCRIPT_BEFORE_TASK
    start_point = find_start_interaction(scripts, n_interaction)
    script = scripts[n_interaction]
    execute_interaction(script, aup, folder, start_point)


def speak_after_item(aup, i_task, i_item):
    """
    NOTE! This is a different kind of script:
        The internal array represents after which item the line is said.
        It assumes ALWAYS 2 lines after item
    """
    folder = INTERACTIONS_FOLDER + "/during_task"
    i_item_h = i_item +1 # "Human readable"
    scripts = SCRIPT_AFTER_ITEM
    if i_item_h in scripts[i_task]:
        wait_for_kid(msg = "Waiting for robot to stop talking")
        i_line = 0
        for script_i_task in range(i_task +1):
            script = scripts[script_i_task]
            if script_i_task == i_task:
                i_line += script.index(i_item_h)
            else:
                i_line += len(script)
        print("I line {}".format(i_line))
        execute_interaction([2], aup, folder, i_line*2) # SUPER HACKY!!


def speak_unknown(aup, n_interaction):
    """
    Disclaimer: This function has been done very hastily and hacky
    """
    folder = INTERACTIONS_FOLDER + "/idk"
    # NOTE Because 0 is Practice
    start_point =  n_interaction -1 
    execute_interaction([1], aup, folder, start_point)


def speak_after_task(aup, n_interaction):
    folder = INTERACTIONS_FOLDER + "/after_task"
    scripts = SCRIPT_AFTER_TASK
    start_point = find_start_interaction(scripts, n_interaction)
    script = scripts[n_interaction]
    execute_interaction(script, aup, folder, start_point)


def speak_finish_experiment(aup):
    folder = INTERACTIONS_FOLDER + "/finish_experiment"
    script = SCRIPT_FINISH
    execute_interaction(script, aup, folder)


# TASKS

def execute_task(task, i_task, aup, words_folder):
    """
    Plays the game: waits for kind input and then says translation
    """
    n_words = len(task.word_order)
    for i in range(n_words):
        word = task.word_order[i]
        results_name = "task_{:d}-word_{:0>2d}_{:s}".format(
                i_task+1, i+1, word)
        results_path = join(p_folder, results_name)
        target_pitch = wait_for_kid(word, results_path)
        if word in UNKNOWN_WORDS:
            speak_unknown(aup, i_task)
        else:
            play_file(word, target_pitch, words_folder, aup)
        speak_after_item(aup, i_task, i)


def execute_tasks(list_tasks, aup, words_folder):
    n_tasks = len(list_tasks)
    
    speak_start_experiment(aup)
    
    for i in range(n_tasks):

        
        task = list_tasks[i]
        print("Starting task {}/{}; category: {}".format(
                i+1, n_tasks, task.category))
        raw_input("Press ENTER to continue")

        speak_before_task(aup, i)
        
        execute_task(task, i, aup, words_folder)
        
        print("Finished task {}/{}".format(i+1, n_tasks))
        raw_input("Press ENTER to finish task")
        speak_after_task(aup, i)
    speak_finish_experiment(aup)


def get_last_participant_id(p_data_folder):
    list_participants = listdir(p_data_folder)
    list_participants.sort(reverse=True)
    participant = None
    for participant in list_participants:
        if "id" in participant:
            break
    if participant:
        last_id = participant.split("-")[0].split("_")[1]
        return int(last_id)
    else:
        return 0
    


def find_participant_folder(participant_id, p_data_folder):
    list_participants = listdir(p_data_folder)
    id_code = "id_{:0>3d}".format(participant_id)
    for participant in list_participants:
        if id_code in participant:
            return participant
    return None


def get_participant_id(p_data_folder):
    last_id = get_last_participant_id(p_data_folder)
    participant_id = None
    while not participant_id:
        participant_input = raw_input(
                "Participant ID? - Empty = {:>2d}: ".format(last_id + 1))
        if participant_input:
            try:
                participant_id = int(participant_input)
            except ValueError:
                print("ERROR: {} is not a valid integer".format(
                        participant_input))
        else:
            participant_id = last_id +1 
    print("Participant {:>2d}".format(participant_id))
    p_folder = find_participant_folder(
            participant_id, p_data_folder)
    if p_folder:
        if input_boolean("A folder for participant id {:0>3d} ".format(
                                 participant_id)
                         + "already exists: \"{}\"".format(p_folder)
                         + ", delete? (y/N) - Empty = NO: ",
                         False):
            rmtree(abspath(join(p_data_folder, p_folder)))
        else:
            return get_participant_id(p_data_folder)
    return participant_id



def get_entrainment_condition():
    entrainment = input_boolean(
            "Entrainment condition (y/N) - Empty = NO: ", False)
    print("Entrainment condition: {}".format(bool(entrainment)))
    return entrainment


def set_configuration(p_data_folder):
    
    global participant_id
    participant_id = get_participant_id(p_data_folder)
    
    global entrainment
    entrainment = get_entrainment_condition()
    
    global p_folder
    p_folder = abspath(join(p_data_folder,"id_{:0>3d}-entrainment_{}".format(
            participant_id, entrainment)))
    makedirs(p_folder) # At this point it shouldn't exist


def main():
    # Parse properties
    f_tasks = FILENAME_TASKS
    p_data_folder = PARTICIPANTS_DATA_FOLDER
    words_folder = WORDS_FOLDER
#    interactions_folder = INTERACTIONS_FOLDER
    ip = IP
    port = PORT
    
    if not exists(p_data_folder):
        makedirs(p_data_folder)
    
    set_configuration(p_data_folder)

    if DEBUG:
        debug = input_boolean(
                "WARNING: Debug mode doesn't use the robot! Continue debug? (y/N) ",
                False)
    if debug:
        aup = AudioPlayerMock
        global be_mngr
        be_mngr = BehaviorManagerMock
    else:
        aup = create_proxy("ALAudioPlayer", ip, port)
        global be_mngr
        be_mngr = create_proxy("ALBehaviorManager", ip, port)
        
    
    list_tasks = read_task_lists(f_tasks)
    execute_tasks(list_tasks, aup, words_folder)
    
    


if __name__ == "__main__":
    main()
