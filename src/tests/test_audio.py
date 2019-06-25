#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 23:55:16 2019

@author: breixo
"""

from audio_utils import record_manual, record_automatic, record_to_file


def demo_automatic():
    print("Wait in silence to begin recording; wait in silence to terminate")
    sample_width, data = record_automatic()
    record_to_file('demo.wav', data, sample_width)
    print("done - result written to demo.wav")


def demo_manual():
    sample_width, data = record_manual()
    record_to_file('demo.wav', data, sample_width)
    print("done - result written to demo.wav")

def main():
#    demo_automatic()
    demo_manual()

if __name__ == '__main__':
    main()
    
    