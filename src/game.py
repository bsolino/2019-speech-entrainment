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
from audio_utils import find_threshold, record_full_manual, record_to_file
from time import sleep
from praat_utils import extract_features, parse_mean_pitch
from distutils.util import strtobool

# Local data
from game_constants import FILENAME_TASKS, PARTICIPANTS_DATA_FOLDER
# NAO Data
from game_constants import NAO_FOLDER, WORDS_FOLDER_TEMPLATE, INTERACTIONS_FOLDER_TEMPLATE
#from game_constants import  WORDS_NELLEKE, WORDS_JUDITH
# Voice Data
from game_constants import \
        PITCH_WORDS, SPEED_WORDS, \
        PITCH_INTERACTIONS_ENTRAINMENT, PITCH_INTERACTIONS_CONTROL, \
        SPEED_INTERACTIONS
# Entrainment
from game_constants import MIN_PITCH, MAX_PITCH, ROUND_STEP
# Interaction scripts
from game_constants import SCRIPT_START, SCRIPT_BEFORE_TASK, INDICATOR_AFTER_ITEM, SCRIPT_AFTER_ITEM, SCRIPT_UNKNOWN, SCRIPT_AFTER_TASK, SCRIPT_FINISH
# Break-related data
from game_constants import SCRIPT_BREAK, SCRIPT_BREAK_BRANCHED_ANIMATIONS, SCRIPT_BREAK_BRANCHED_INTERACTIONS

from test_utils import AudioPlayerMock, BehaviorManagerMock, MotionMock

NAO_WORDS_FOLDER_TEMPLATE = NAO_FOLDER + WORDS_FOLDER_TEMPLATE
#WORDS_FOLDER = NAO_FOLDER + WORDS_NELLEKE
#WORDS_FOLDER = NAO_FOLDER + WORDS_JUDITH
NAO_INTERACTIONS_FOLDER_TEMPLATE = NAO_FOLDER + INTERACTIONS_FOLDER_TEMPLATE

UNKNOWN_WORDS = ["ear", "walk"]
#UNKNOWN_WORDS = [] # To deactivate unknowns

#CONSTANTS
DEBUG = True

# CONFIGURATION GLOBAL VARIABLES
participant_id = None
entrainment = None
p_folder = None
# Derived
pitch_interactions = None
speed_interactions = None
pitch_words = None
speed_words = None
interactions_folder = None
words_folder = None

# HOTFIX GLOBAL VARIABLES
last_target_pitch = 240  # For issues with entrainment failures. 240 as is average value
be_mngr = None # BEHAVIOR MANAGER - here for simplicity
motion = None


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
        sample_width, audio_data = record_full_manual()
        mean_pitch = analyze_audio_data(base_path, audio_data, sample_width)
        if mean_pitch:
            target_pitch = round_and_bound_pitch(mean_pitch)
            global last_target_pitch
            last_target_pitch = target_pitch
        else:
            print("WARNING: Couldn't entrain")
            target_pitch = last_target_pitch
    else:
        raw_input(msg) # Temporal solution
    if not entrainment:
       target_pitch = "base"
    return target_pitch


def play_file(filename, target_freq, folder, aup):
    word_file = find_word_file(filename, folder, target_freq)
    print(word_file)
    aup.post.playFile(word_file)
#    aup.playFile(word_file) # Testing blocking the call


# ROBOT UTTERANCES

def execute_interaction(script, aup, folder, start_point = 0):
    i_sentence = start_point
    for i_action in range(len(script)):
        action = script[i_action]
        if type(action) is int:
            n_sentences = action
            i_last_sentence = i_sentence + n_sentences
            i_sentence += 1
            for i_sentence in range(i_sentence, i_last_sentence+1):
                audio_file = folder + "/{:0>2d}-base.wav".format(i_sentence)
                print("Interaction {} of {}".format(
                        i_sentence, i_last_sentence))
                aup.playFile(audio_file)
                if (i_action+1) < len(script) and script[i_action+1] != "wait":
                    print("Pausing")
                    sleep(0.7)
        elif action == "wait":
            wait_for_kid()
        elif type(action) is float:
            sleep(action)
        elif action == "rest":
            print("Resting")
            motion.rest()
            motion.setBreathEnabled("Body", False)
        elif action == "wake up":
            print("Waking up")
            motion.wakeUp()
            motion.setBreathEnabled("Body", True)
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
    folder = interactions_folder + "/start_experiment"
    script = SCRIPT_START
    execute_interaction(script, aup, folder)


def speak_before_task(aup, n_interaction):
    folder = interactions_folder + "/before_task"
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
    folder = interactions_folder + "/during_task"
    i_item_h = i_item +1 # "Human readable"
    indicators = INDICATOR_AFTER_ITEM
    scripts = SCRIPT_AFTER_ITEM
    if i_item_h in indicators[i_task]:
        wait_for_kid(msg = "Waiting for robot to stop talking")
        i_line = 0
        for indicator_i_task in range(i_task +1):
            indicator = indicators[indicator_i_task]
            if indicator_i_task == i_task:
                i_line += indicator.index(i_item_h)
            else:
                i_line += len(indicator)
            script = scripts[i_line]
        print("I line {}".format(i_line))
        execute_interaction(script, aup, folder, i_line*2) # SUPER HACKY!!


def speak_unknown(aup, n_interaction):
    """
    Disclaimer: This function has been done very hastily and hacky
    """
    folder = interactions_folder + "/idk"
    # NOTE Because 0 is Practice
    start_point =  n_interaction -1 
    scripts = SCRIPT_UNKNOWN
    script = scripts[start_point]
    execute_interaction(script, aup, folder, start_point)


def speak_after_task(aup, n_interaction):
    folder = interactions_folder + "/after_task"
    scripts = SCRIPT_AFTER_TASK
    start_point = find_start_interaction(scripts, n_interaction)
    script = scripts[n_interaction]
    execute_interaction(script, aup, folder, start_point)


def speak_finish_experiment(aup):
    folder = interactions_folder + "/finish_experiment"
    script = SCRIPT_FINISH
    execute_interaction(script, aup, folder)


def speak_break(aup):
    folder = interactions_folder + "/break/"
    scripts = SCRIPT_BREAK
    animations = [a for a in SCRIPT_BREAK_BRANCHED_ANIMATIONS]
    branching_interactions = SCRIPT_BREAK_BRANCHED_INTERACTIONS
    
    n_interaction = 0
    while n_interaction < len(scripts):
        script = scripts[n_interaction]
        starting_point = find_start_interaction(scripts, n_interaction)
        
        print("Start break part {}".format(n_interaction+1))
        execute_interaction(script, aup, folder, starting_point)
        
        print("Finish break part {}".format(n_interaction+1))
        
        if n_interaction in branching_interactions:
            selection = None
            if len(animations) > 0:
                if len(animations) > 1:
                    while not selection:
                        msg = "Select animation:\n"
                        for i in range(len(animations)):
                            msg += "{}: {}\n".format(i+1, animations[i])
                        selection_input =  raw_input(msg)
                        if selection_input:
                            try:
                                selection = int(selection_input)
                            except ValueError:
                                print("ERROR: {} is not a valid integer".format(
                                        selection_input))
                        if selection <= 0 or selection > len(animations):
                            selection = None
                        else:
                            selection -= 1
                            break
                    animation = animations.pop(selection)
                else:
                    print("Last Animation")
                    animation = animations.pop()
                
                
                n_interaction += 1
                
                script = scripts[n_interaction]
                starting_point = find_start_interaction(scripts, n_interaction)
                
                execute_interaction(script, aup, folder, starting_point)
                be_mngr.runBehavior(animation)
        n_interaction += 1
            
        
    
    
    


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
    
    # Artificially change the pitch, to simulate entrainment
    # TODO Clean hack
    if entrainment:
        global pitch_interactions, interactions_folder
        pitch_interactions = PITCH_INTERACTIONS_ENTRAINMENT
        interactions_folder = NAO_INTERACTIONS_FOLDER_TEMPLATE.format(
                speed_interactions, pitch_interactions)
    
    for i in range(n_tasks):
        # TODO Hotfix
        if i == 3:
            raw_input("Press ENTER to start break")
            speak_break(aup)
        
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
    
    # Derived values
    global pitch_interactions, speed_interactions, \
            pitch_words, speed_words,\
            interactions_folder, words_folder
#    if entrainment:
#        pitch_interactions = PITCH_INTERACTIONS_ENTRAINMENT
#    else:
#        pitch_interactions = PITCH_INTERACTIONS_CONTROL
    pitch_interactions = PITCH_INTERACTIONS_CONTROL
    pitch_words = PITCH_WORDS
    speed_words = SPEED_WORDS
    speed_interactions = SPEED_INTERACTIONS
    interactions_folder = NAO_INTERACTIONS_FOLDER_TEMPLATE.format(
            speed_interactions, pitch_interactions)
    words_folder = NAO_WORDS_FOLDER_TEMPLATE.format(
            speed_words, pitch_words)


def check_audio():
    find_threshold(1)


def main():
    # Parse properties
    f_tasks = FILENAME_TASKS
    p_data_folder = PARTICIPANTS_DATA_FOLDER
#    words_folder = WORDS_FOLDER
#    interactions_folder = INTERACTIONS_FOLDER
    ip = IP
    port = PORT
    
    check_audio()
    
    if not exists(p_data_folder):
        makedirs(p_data_folder)
    
    set_configuration(p_data_folder)

    if DEBUG:
        debug = input_boolean(
                "WARNING: Debug mode doesn't use the robot! Continue debug? (y/N) ",
                False)
    global be_mngr, motion
    if debug:
        aup = AudioPlayerMock
        be_mngr = BehaviorManagerMock
        motion = MotionMock
    else:
        aup = create_proxy("ALAudioPlayer", ip, port)
        
        be_mngr = create_proxy("ALBehaviorManager", ip, port)
        motion = create_proxy("ALMotion", ip, port)
    
    list_tasks = read_task_lists(f_tasks)
    execute_tasks(list_tasks, aup, words_folder)
    
    


if __name__ == "__main__":
    main()
