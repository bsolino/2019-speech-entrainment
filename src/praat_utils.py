#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 07:29:25 2019

@author: breixo
"""

from os.path import join, abspath
from subprocess import call

PRAAT_SCRIPT_PATH = abspath(join("..", "misc"))
EXTRACT_PRAAT_SCRIPT = join(PRAAT_SCRIPT_PATH, "extract_features.praat")
"""
    sentence filename
    sentence outfilename
    boolean extract_intensity 1
    boolean extract_pitch 1
    boolean extract_durations 1
    boolean extract_jitter_shimmer 1

"""
SCRIPT_PITCH_OPTION = ["0", "1", "0", "0"]
PRAAT_LOCATION = "praat"

def call_praat(script, args = None):
    praat_call = [
            PRAAT_LOCATION,
            "--run"
            ]
    praat_call.append(script)
    if args:
        try:
            praat_call.extend(args)
        except:
            praat_call.append(args)
    
    result = call(praat_call)
    assert (result == 0)


def adapt():
    pass # TODO


def parse_feature_line(line):
    key, value = line.strip().split(",")
    return key, float(value)


def parse_mean_pitch(return_file):
    with open(return_file, "r") as f:
        lines = f.readlines()
    for line in lines:
        feature, value = parse_feature_line(line)
        if feature == "pitch_mean":
            return value
    raise KeyError("pitch_mean not found in file {}".format(return_file))


def parse_features(return_file):
    with open(return_file, "r") as f:
        lines = f.readlines()
    features = dict()
    for line in lines:
        key, value = parse_feature_line(line)
        features[key] = value
    return features


def extract_features(sound_file, return_file):
    sound_file = abspath(sound_file)
    return_file = abspath(return_file)
    
#    praat_call = [
#            PRAAT_LOCATION,
#            "--run",
#            EXTRACT_PRAAT_SCRIPT,
#            sound_file,
#            return_file
#            ] + SCRIPT_PITCH_OPTION
#    result = call(praat_call)
#    assert (result == 0)  # Check that the script worked
    args = [sound_file, return_file] + SCRIPT_PITCH_OPTION
    call_praat(EXTRACT_PRAAT_SCRIPT, args)

