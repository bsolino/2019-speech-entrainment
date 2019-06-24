#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 22:26:57 2019

@author: breixo
"""

from os import listdir
from os.path import join, isfile, isdir, basename
from nao_utils import create_proxy, IP, PORT

PITCH = 1.15
#SPEED = .75 * 100
SPEED = 1 * 100
LANG = "Dutch"

NAO_FOLDER = "/home/nao/entrainment/interactions_s{:0>3d}_p{:.2f}/base".format(
        SPEED, PITCH)
INTERACTIONS_FOLDER = join("data", "interaction")

VERBOSE = True

class Sentence:
    
    def __init__(self, category, number, text):
        self.category = category
        self.number = number
        self.text = text
    
    
    def get_route(self):
        name = "{:0>2d}-base.wav".format(self.number)
        return join(self.category, name)
    
    def say_to_file(self, tts, destination_folder):
        """
        Use TTS to say the words to a file (internal in the robot)
        """
        route = join(destination_folder, self.get_route())
        if VERBOSE:
            print(self)
        tts.sayToFile(self.text, route)
        
    
    def __repr__(self):
        return "{:<15}: \"{}\"".format(self.get_route(), self.text)


def configure_voice(tts, language, pitch, speed):
    """
    Prepare the voice to be used by the TTS system

    Default: All at 1. (no modifiers)
    """
    tts.setLanguage(language)
    tts.setParameter("pitchShift", pitch)
    tts.setParameter("speed", speed)
#    tts.setVoice(


def parse_category(filename):
    aux = basename(filename)
    return aux[:aux.find(".")].lower().strip()


def parse_sentence_text(line):
    if not '"' in line:
        return None
    text = line[line.find('"')+1:]
    return text[:text.find('"')].strip()


def parse_sentences_file(filename):
    category = parse_category(filename)
    with open(filename, "r") as f:
        lines = f.readlines()
        sentences_list = list()
        counter = 0
        for line in lines:
            text = parse_sentence_text(line)
            if text:
                counter += 1
                sentence = Sentence(category, counter, text)
                sentences_list.append(sentence)
                if VERBOSE:
                    print(sentence)
        return sentences_list


def parse_interactions_folder(path):
    assert isdir(path)
    files = [join(path, f) for f in listdir(path)
            if isfile(join(path, f))]
    return files



def retrieve_word_files(folder):
    """
    Copy files from robot's internal storage to the physical computer
    """
    pass  # TODO?
#    import os
#    import paramiko
#    
#    ssh = paramiko.SSHClient() 
#    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
#    ssh.connect(server, username=username, password=password)
#    sftp = ssh.open_sftp()
#    sftp.put(localpath, remotepath)
#    sftp.close()
#    ssh.close()


def main():
    # Parse properties
    origin_folder = INTERACTIONS_FOLDER
    destination_folder = NAO_FOLDER
    ip = IP
    port = PORT
    pitch = PITCH
    speed = SPEED
    language = LANG


    tts = create_proxy("ALTextToSpeech", ip, port)
    configure_voice(tts, language, pitch, speed)
    
    interaction_files = parse_interactions_folder(origin_folder)
    for filename in interaction_files:
        list_sentences = parse_sentences_file(filename)
        for sentence in list_sentences:
           sentence.say_to_file(tts, destination_folder)
        retrieve_word_files(destination_folder)


if __name__ == "__main__":
    main()
