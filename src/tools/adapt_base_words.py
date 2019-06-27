#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 15:59:12 2019

@author: breixo
"""

from os import listdir
from os.path import join, abspath, pardir
from praat_utils import adapt

BASE_WORDS_FOLDER = abspath(join(
        pardir, "resources", "words_s075_p1.00", "experiment"))

#MIN_PITCH = 50
#MAX_PITCH = 500
MIN_PITCH = 130
MAX_PITCH = 350

STEP = 5


def round_to_step(x):
    base = STEP
    value = int(base * round(float(x)/base))
    ret = max(MIN_PITCH, min(MAX_PITCH, value))
    print("Original value = {}; Rounded = {}; returns = {}".format(x, value, ret))


failed = {}
for f in listdir(BASE_WORDS_FOLDER):
    if not "base.wav" in f:
        continue
    original_file = join(BASE_WORDS_FOLDER, f)
    word = f.split("-")[0]
    base_word = join(BASE_WORDS_FOLDER, word)
    for target_pitch in range(MIN_PITCH, MAX_PITCH+1, STEP):
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

#if __name__ == "__main__":
#    main()