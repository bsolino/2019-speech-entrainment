#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#import os

import praat_utils

def main():
    sound_file = "demo.wav"
#    return_file = os.path.abspath("return/dance-base.txt")
#    praat_utils.extract_features(sound_file, return_file)
    print(praat_utils.extract_features(sound_file))


if __name__ == "__main__":
    main()