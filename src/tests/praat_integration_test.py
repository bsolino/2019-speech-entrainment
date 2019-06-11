#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import subprocess
import os

EXTRACT_PRAAT_SCRIPT = "../misc/extract_features.praat"
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

    
def main():
    sound_file = "../../words/dance-base.wav"
    return_file = os.path.join(os.getcwd(), "return/dance-base.txt")
    praat_call = [
            PRAAT_LOCATION,
            "--run",
            EXTRACT_PRAAT_SCRIPT,
            sound_file,
            return_file
            ] + SCRIPT_PITCH_OPTION
    result = subprocess.call(praat_call)
    with open(return_file, "r") as f:
        print(f.readlines())


if __name__ == "__main__":
    main()