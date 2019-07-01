#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 15:59:12 2019

@author: breixo
"""

from os import listdir, walk
from os.path import join, abspath, pardir
from praat_utils import adapt

from game_constants import MIN_PITCH, MAX_PITCH, ROUND_STEP


#MIN_PITCH = 50
#MAX_PITCH = 500

ORIGIN_FOLDER = abspath(join(pardir, "resources", "to_adapt"))



def round_to_step(x):
    base = ROUND_STEP
    value = int(base * round(float(x)/base))
    ret = max(MIN_PITCH, min(MAX_PITCH, value))
    print("Original value = {}; Rounded = {}; returns = {}".format(x, value, ret))


def adapt_all_files(folder):
    failed = {}
    for f in listdir(folder):
        if not "base.wav" in f:
            continue
        original_file = join(folder, f)
        word = f.split("-")[0]
        base_word = join(folder, word)
        for target_pitch in range(MIN_PITCH, MAX_PITCH+1, ROUND_STEP):
            target_file = "{}-{}.wav".format(base_word, target_pitch)
            try:
                adapt(original_file, target_file, target_pitch)
            except AssertionError:
                failed[word] = target_pitch
        
    failed_words = failed.keys()
    failed_words.sort()
    max_freq = 0
    for word in failed_words:
        failed_freq = failed[word]
        print("{:>15s} - freq = {:>3d}".format(word, failed_freq))
        if failed_freq > max_freq:
            max_freq = failed_freq
    print("Max failed freq = {}".format(max_freq))
    

if __name__ == "__main__":
    #    main()
    origin_folder = ORIGIN_FOLDER
    folders = [p[0] for p in walk(origin_folder)]
    for folder in folders:
        adapt_all_files(folder)