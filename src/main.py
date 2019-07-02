#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 13:01:19 2019

@author: breixo
"""

"""
Hack to Silence PyAudio warnings
"""

import sys
from os.path import join
sys.stderr = open(join("return","logfile.txt"), 'ab')

execfile('game.py')