#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 02:28:02 2019

@author: breixo
"""

from distutils.util import strtobool


class ExperimentWords:
    
    def __init__(self, data):
        self.data = data
    
    def get_categories(self):
        return self.data.keys()
    
    def get_data(self):
        return self.data()
    
    def get_all_words(self):
        all_words = list()
        for list_words in self.data.values():
            all_words += list_words
        return all_words

def parse_word_info(line):
    """
    Extracts the word from a line of a list of words
    """
    # TODO Need more info about word list files
    line = line.lower().strip()
    return line.split(" ")


def add_word(data, category, is_target, word):
    """
    Add word to dictionary
    """
    list_words = data.get(category, list())
    list_words.append(word)
    data[category] = list_words


def parse_file(filename):
    """
    Creates a ExperimentWords object from a file
    """
    with open(filename, "r") as f:
        lines = f.readlines()
        data = dict()
        for line in lines:
            word_info = parse_word_info(line)
            category = word_info[0]
            is_target = bool(strtobool(word_info[1]))
            word = word_info[2]
            add_word(data, category, is_target, word)
        print(data)
        return ExperimentWords(data)