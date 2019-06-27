#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os

import praat_utils
from datetime import datetime
from audio_utils import record_manual
from game import analyze_audio_data


def call_praat_test():
    sound_file = os.path.join("return", "test", "demo.wav")
    return_file = os.path.abspath("return/tmp/extract_features.tmp")
#    praat_utils.extract_features(sound_file, return_file)
    praat_utils.extract_features(sound_file, return_file)
    print(praat_utils.parse_mean_pitch(return_file))


def time_analyze_recording():
    base_path = os.path.join("return", "test", "test_analyze_time")
    
    sample_width, audio_data = record_manual()
    start = datetime.now()
    mean_pitch = analyze_audio_data(base_path, audio_data, sample_width)
    end = datetime.now()
    
    print("Time: {} - Mean pitch: {}".format(
            str(end - start), mean_pitch))


def main():
#    call_praat_test()
    time_analyze_recording()


if __name__ == "__main__":
    main()