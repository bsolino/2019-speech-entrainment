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
#PITCH_WORDS = 1.15 # Literally doesn't work
SPEED_WORDS = int(.75 * 100)
#PITCH_INTERACTIONS = 1.15
PITCH_INTERACTIONS = 1.00 # Test, for adaptation
#SPEED_INTERACTIONS = .75 * 100
SPEED_INTERACTIONS = 1 * 100
LANG_EN = "English"
LANG_NL = "Dutch"


# Folders
WORDS_FOLDER_TEMPLATE = "words_s{:0>3d}_p{:.2f}/"
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