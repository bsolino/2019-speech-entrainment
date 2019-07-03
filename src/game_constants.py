#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 18:46:06 2019

@author: breixo
"""

from os import pardir
from os.path import join, abspath


"""
Local data
"""
FILENAME_TASKS = join("data", "tasks", "selected_tasks.txt")
WORDS_FILE = join("data", "list_words.txt")

PARTICIPANTS_DATA_FOLDER = abspath(join(pardir, "participant_data"))

"""
NAO data
"""
# TTS settings
PITCH_WORDS = 1
#PITCH_WORDS_ENTRAINMENT = 1.15 # Literally doesn't work
SPEED_WORDS = int(.75 * 100)
PITCH_INTERACTIONS_ENTRAINMENT = 1.15
PITCH_INTERACTIONS_CONTROL = 1.07
#PITCH_INTERACTIONS = 1.00 # Test, for adaptation
#SPEED_INTERACTIONS = .75 * 100
SPEED_INTERACTIONS = 1 * 100


LANG_EN = "English"
LANG_NL = "Dutch"


# Folders
WORDS_FOLDER_TEMPLATE = "words_s{:0>3d}_p{:.2f}/"
WORDS_JUDITH = "words_judith/"
WORDS_NELLEKE = "words_nelleke/"
INTERACTIONS_FOLDER_TEMPLATE = "interactions_s{:0>3d}_p{:.2f}/"
NAO_FOLDER = "/home/nao/entrainment/"
GENERATION_FOLDER = "generation/"

"""
Entrainment constants
"""
MIN_PITCH = 130
MAX_PITCH = 350
ROUND_STEP = 5


"""
NAO Connection
"""
IP_WIFI = "192.168.0.199"
IP_CABLE = "192.168.0.197"

#IP = IP_WIFI
IP = IP_CABLE

PORT = 9559


"""
Interaction scripts
"""
SCRIPT_START = [
        "animations/Stand/Emotions/Neutral/Hello_1",
        1.,
        1,
        "animations/Stand/Gestures/Me_2",
        1,
        "animations/Stand/Gestures/You_3",
        0.1,
        1,
        "wait",
        "animations/Stand/Emotions/Positive/Enthusiastic_1",
        1,
        0.3,
        "animations/Stand/BodyTalk/Speaking/BodyTalk_14",
        1,
        "animations/Stand/Emotions/Positive/Excited_3",
        1,
        0.3,
        "animations/Stand/BodyTalk/Speaking/BodyTalk_11",
        0.5,
        2,
        "wait",
        "animations/Stand/Gestures/Me_7",
        2,
        "animations/Stand/BodyTalk/Speaking/BodyTalk_2",
        1,
        "animations/Stand/BodyTalk/Thinking/Remember_1",
        1,
        "animations/Stand/Emotions/Positive/Excited_3",
        1,
        "wait",
        # Locked
        "animations/Stand/BodyTalk/Speaking/BodyTalk_5",
        1,
        "animations/Stand/BodyTalk/Speaking/BodyTalk_21",
        1,
        "animations/Stand/Emotions/Neutral/Determined_1",
        1
        ]
SCRIPT_BEFORE_TASK = [
        [               # Practice round
                3,
                "wait",
                2
                ],
        [               # Task 1
                1,
                "wait",
                2,
                "wait",
                1
                ],
        [               # Task 2
                1,
                "wait",
                1
                ],
        [               # Task 3
                2,
                "wait",
                1
                ],
        [               # Task 4
                2,
                "wait",
                1
                ]
        ]
SCRIPT_AFTER_ITEM = [
        [1, 2],    # Practice
        [],
        [],
        [],
        []
#        [1, 2, 5],    # Practice
#        [6],            # Task 1
#        [6],            # Task 2
#        [6],            # Task 3
#        [7]             # Task 4
        ]
SCRIPT_AFTER_TASK = [
        [1],     # Practice - Nothing
        [1],    # Task 1
        [1],    # Task 2
        [1],    # Task 3
        [1]     # Task 4
        ]
SCRIPT_FINISH = [
        5,
        "wait",
        4
        ]
