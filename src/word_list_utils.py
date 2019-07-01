#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 02:28:02 2019

@author: breixo
"""

from distutils.util import strtobool


class WordInfo:
    
    def __init__(self, word, is_target, category, pronunciation):
        self.word = word
        self.is_target = is_target
        self.is_sentence = bool(pronunciation)
        if pronunciation:
            self.pronunciation = pronunciation
        else:
            self.pronunciation = word
        self.category = category


    def __repr__(self):
        return self.word + ": " + str(self.is_target)


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
    word_info = line.split(";")
    word_info = [word.strip() for word in word_info]
#    for i in range(len(word_info)):
#        word_info[i] = word_info[i].strip()

    category = word_info[0]
    is_target = bool(strtobool(word_info[1]))
    word = word_info[2]
    if len(word_info) > 3:
        pronunciation = word_info[3]
    else:
        pronunciation = None
    return WordInfo(word, is_target, category, pronunciation)


def add_word(data, word_info):
    """
    Add word to dictionary
    """
    category = word_info.category
    list_words = data.get(category, list())
    list_words.append(word_info)
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
            add_word(data, word_info)
        print(data)
    return ExperimentWords(data)