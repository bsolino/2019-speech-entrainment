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
        "wake up",
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
        "animations/Stand/BodyTalk/Speaking/BodyTalk_5",
        1,
        "animations/Stand/BodyTalk/Speaking/BodyTalk_21",
        1,
        "animations/Stand/Emotions/Neutral/Determined_1",
        1,
        "rest"
        ]
SCRIPT_BEFORE_TASK = [
        [               # Practice round
                "wake up",
                "animations/Stand/Emotions/Positive/Happy_4",
                1,
                "animations/Stand/BodyTalk/Speaking/BodyTalk_12",
                1,
                "animations/Stand/Gestures/ShowFloor_1",
                1,             
                "wait",
                "animations/Stand/BodyTalk/Speaking/BodyTalk_14",
                1,
                "animations/Stand/BodyTalk/Speaking/BodyTalk_10",
                1
                ],
        [               # Task 1
                "animations/Stand/BodyTalk/Speaking/BodyTalk_11",
                1,
                "wait",
                "animations/Stand/Gestures/ShowFloor_1",
                1,
                "animations/Stand/Gestures/Me_3",
                1,
                "wait",
                "animations/Stand/Gestures/Coaxing_1",
                1
                ],
        [               # Task 2
                0.5,
                "animations/Stand/Gestures/ShowFloor_1",
                1,
                "wait",
                "animations/Stand/Emotions/Positive/Enthusiastic_1",
                1
                ],
        [               # Task 3
                "animations/Stand/Gestures/Explain_3",
                1,
                1.0,
                "animations/Stand/Gestures/You_5",
                1,
                "wait",
                "animations/Stand/Emotions/Neutral/Determined_1",
                1
                ],
        [               # Task 4
                "animations/Stand/Gestures/Explain_2",
                1,
                "animations/Stand/Gestures/You_4",
                1,
                "wait",
                "animations/Stand/Gestures/Coaxing_2",
                1
                ]
        ]
# Marks if there is an utterance after an item
INDICATOR_AFTER_ITEM = [
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

"""
NOTE! This is different from the others. There is a script for each time
"speak_after_item()" is called. Those calls are marked in
"INDICATOR_AFTER_ITEM"
"""
SCRIPT_AFTER_ITEM = [
        [
                "animations/Stand/Emotions/Positive/Happy_4",
                1,
                "animations/Stand/BodyTalk/Speaking/BodyTalk_21",
                1
                ],
        [
                    "animations/Stand/Emotions/Positive/Enthusiastic_1",
                    1,
                    "animations/Stand/Gestures/Explain_3",
                    1
                    ]
        ]

"""
NOTE! This script has the same special behavior as SCRIPT_AFTER_ITEM
"""
SCRIPT_UNKNOWN = [
        #1st idk
        [
                "animations/Stand/Emotions/Neutral/Confused_1",
                1
                ],
        #2nd idk
        [
                 "animations/Stand/Waiting/ScratchHead_1",
                1
                ],
        #3rd idk
        [
                 "animations/Stand/Waiting/Think_1",
                1
                ],
        #4th idk
        [
                 "animations/Stand/Waiting/Think_4",
                1
                ]
        ]

SCRIPT_AFTER_TASK = [
        [               #Practice
                "animations/Stand/BodyTalk/Speaking/BodyTalk_21",
                1
                ],
        [               # Task 1
                "animations/Stand/Emotions/Positive/Enthusiastic_1",
                1
                ],    
        [               # Task 2
                "animations/Stand/Emotions/Positive/Happy_4",
                1
                ],    
        [               # Task 3
                "animations/Stand/Emotions/Positive/Excited_1",
                0.8, #finish first sentence before starting animation
                1
                ],    
        [               # Task 4
                0.7,
                "animations/Stand/Emotions/Positive/Enthusiastic_1",
                1
                ],    
        ]
SCRIPT_FINISH = [
                "animations/Stand/Gestures/You_5",
                1,
                "animations/Stand/BodyTalk/Speaking/BodyTalk_12",
                1,
                "animations/Stand/BodyTalk/Speaking/BodyTalk_6",
                1,
                "animations/Stand/Emotions/Positive/Happy_4",
                1,
                "animations/Stand/Gestures/You_3",
                1,
                "wait",
                "animations/Stand/BodyTalk/Speaking/BodyTalk_9",
                1,
                0.5,
                "animations/Stand/Gestures/Me_4",
                1,
                0.2,
                "animations/Stand/BodyTalk/Speaking/BodyTalk_21",
                1,
                "animations/Stand/Emotions/Neutral/Hello_1",
                1,
                "rest"
        ]



"""
BREAK RELATED DATA
"""
SCRIPT_BREAK = [
        [
                "animations/Stand/BodyTalk/Speaking/BodyTalk_14",
                1,
                "wait",
                "animations/Stand/BodyTalk/Speaking/BodyTalk_21",
                1,
                "animations/Stand/Emotions/Positive/Excited_3",
                1,
                "animations/Stand/BodyTalk/Speaking/BodyTalk_10",
                1,
                "animations/Stand/Gestures/You_3",
                1,
                "wait",
                "animations/Stand/BodyTalk/Thinking/Remember_1",
                1,
                "animations/Stand/Gestures/You_5",
                1,
                "wait",
                1,
                "wait",
                "animations/Stand/Waiting/Drink_1",
                4.5,
                1,
                "animations/Stand/BodyTalk/Speaking/BodyTalk_2",
                1,
                "animations/Stand/BodyTalk/Speaking/BodyTalk_5",
                1,
                "animations/Stand/BodyTalk/Thinking/Remember_2",
                1,
                "animations/Stand/Gestures/Choice_1",
                1,
                "animations/Stand/Gestures/You_3",
                1
                ],
        [
                1
                ],
        [
                "animations/Stand/Gestures/You_4",
                1
                ],
        [
                1
                ],
        [
                "animations/Stand/Gestures/WhatSThis_14",
                1
                ],
        [],
        [
                "animations/Stand/Gestures/WhatSThis_15",
                1,
                "wait",
                "animations/Stand/Gestures/Me_7",
                1,
                "animations/Stand/Emotions/Neutral/Determined_1",
                1
                ]
        ]
SCRIPT_BREAK_BRANCHED_ANIMATIONS = [
        "animations/Stand/Waiting/Monster_1",
        "animations/Stand/Emotions/Neutral/Sneeze",
        "animations/Stand/Waiting/Bandmaster_1"
        ]
# Index of the interactions where a break happens:
SCRIPT_BREAK_BRANCHED_INTERACTIONS = [0, 2, 4]
