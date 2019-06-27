#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 17:34:59 2019

@author: breixo
"""

from nao_utils import create_proxy
from game import WORDS_FOLDER, MIN_PITCH, MAX_PITCH, ROUND_STEP
from word_list_utils import parse_file, WORDS_FILE

aup = aup = create_proxy("ALAudioPlayer")



words = parse_file(WORDS_FILE).get_all_words()
for word in words:
    word = word.word
    base_file = WORDS_FOLDER + "/" + word
    aup.playFile(base_file + "-base.wav")
    for freq in range(MIN_PITCH, MAX_PITCH+1, ROUND_STEP):
        aup.playFile(base_file + "-{}.wav".format(freq))
    raw_input("ENTER TO CONTINUE")