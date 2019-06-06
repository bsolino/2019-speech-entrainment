#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 16:06:38 2019

@author: breixo
"""

import random
from word_list_utils import parse_file, WORDS_FILE, WordInfo


DISTRIBUTIONS_FILE = "data/tasks/distributions.txt"
TASKS_FILE = "data/tasks/tasks.txt"



class Task:
    
    def __init__(self, category, word_order):
        self.category = category
        self.word_order = word_order



def create_task_list(words, distribution):
    """
    Creates a list for a task based on the distribution.
    Does it so by populating it randomly with words
    """
    targets = []
    fillers = []
    for i in range(len(words)):
        words[i].index = i
        word = words[i]
        if word.is_target:
            targets.append(word)
        else:
            fillers.append(word)
    random.shuffle(targets)
    random.shuffle(fillers)
    task_list = [targets.pop() if insert_target else fillers.pop()
            for insert_target in distribution]
    assert len(fillers) == 0
    assert len(targets) == 0

    return task_list


def parse_distribution_info(line):
    distribution = line.lower().replace("[", "").replace("]", "").split(",")
    distribution = [int(value.strip()) for value in distribution]
    return distribution


def read_distributions(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        list_distributions = []
        for line in lines:
            distribution = parse_distribution_info(line)
            list_distributions.append(distribution)
        print(list_distributions)
    return list_distributions


def save_task_lists(task_lists, filename):
    with open(filename, "w") as f:
        newline = ""
        for category in task_lists.keys():
            value = task_lists[category]
            for task_list in value:
                f.write(newline + category + ": " + str(task_list))
                if not newline:
                    newline = "\n"


def parse_task_line(line):
    line = line.lower()
    category = line[0:line.find(":")].strip()
    line = line[line.find("[")+1:line.find("]")].strip()
    line = line.split(",")
    word_order = list()
    for word_info in line:
        word_finish = word_info.find(":")  # Searches for where the word ends
        if word_finish > 0:
            word = word_info[0:word_info.find(":")].strip()  # Ignores rest
        else:
            word = word_info.strip()
        word_order.append(word)
    return Task(category, word_order)
    

def read_task_lists(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        task_lists = dict()
        

def main():
    words_file = WORDS_FILE
    distributions_file = DISTRIBUTIONS_FILE
    words_data = parse_file(words_file)
    distributions = read_distributions(distributions_file)
    tasks_file = TASKS_FILE
    
    task_lists = {}
    for category in words_data.get_categories():
        category_task_lists = []
        words = words_data.data[category]
        for distribution in distributions:
            task_list = create_task_list(words, distribution)
            category_task_lists.append(task_list)
        task_lists[category] = category_task_lists
    save_task_lists(task_lists, tasks_file)
    

if __name__ == "__main__":
    main()
