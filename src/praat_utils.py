#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 07:29:25 2019

@author: breixo
"""

from os.path import join, abspath
from subprocess import call

PRAAT_SCRIPT_FOLDER = abspath(join("..", "misc"))
EXTRACT_PRAAT_SCRIPT = join(PRAAT_SCRIPT_FOLDER, "extract_features.praat")
"""
    sentence filename
    sentence outfilename
    boolean extract_intensity 1
    boolean extract_pitch 1
    boolean extract_durations 1
    boolean extract_jitter_shimmer 1

"""
EXTRACT_SCRIPT_PITCH_OPTION = ["0", "1", "0", "0"]

ADAPT_PRAAT_SCRIPT = join(join(PRAAT_SCRIPT_FOLDER, "adapt.praat"))


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


def adapt(in_sound, out_sound, target_mean_pitch):
    """
    sentence in_fname
    sentence out_fname
    integer syllable_count
    real target_rate_syll_per_s
    real target_intensity_mean_db
    real target_pitch_mean_hz
"""
    args = [
            in_sound,
            out_sound,
            "-1",
            "-1",
            "-1",
            str(target_mean_pitch)
            ]
    call_praat(ADAPT_PRAAT_SCRIPT, args)


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
#            ] + EXTRACT_SCRIPT_PITCH_OPTION
#    result = call(praat_call)
#    assert (result == 0)  # Check that the script worked
    args = [sound_file, return_file] + EXTRACT_SCRIPT_PITCH_OPTION
    call_praat(EXTRACT_PRAAT_SCRIPT, args)

