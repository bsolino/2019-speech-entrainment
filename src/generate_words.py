#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import paramiko
from nao_utils import create_proxy, IP, PORT
from word_list_utils import parse_word

PITCH = 1
SPEED = 1
LANG = "English"

FILENAME = "list_words.txt"
FOLDER = "words"


def read_list(filename):
    """
    From a file, parse the words to say
    """
    with open("filename", "r") as f:
        lines = f.readlines()
        n_lines = len(lines)
        list_words = [None] * n_lines
        for i in range(n_lines):
            line = lines[i]
            list_words[i] = parse_word(line)
        return list_words


def configure_voice(tts, language, pitch, speed):
    """
    Prepare the voice to be used by the TTS system

    Default: All at 1. (no modifiers)
    """
    tts.setLanguage(language)
    tts.setParameter("pitchShift", pitch)
    tts.setParameter("speed", speed)
#    tts.setVoice(


def create_word_files(tts, list_words, folder):
    """
    Use TTS to say the words to a file (internal in the robot)
    """
    for word in list_words:
        route = "/" + folder + "/" + word
        tts.sayToFile(word, route + ".raw")
        tts.sayToFile(word, route + ".wav")  # TODO: Choose which one


def retrieve_word_files(folder):
    """
    Copy files from robot's internal storage to the physical computer
    """
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
    filename = FILENAME
    folder = FOLDER
    ip = IP
    port = PORT
    pitch = PITCH
    speed = SPEED
    language = LANG

    list_words = read_list(filename)
    tts = create_proxy("ALTextToSpeech", ip, port)
    configure_voice(tts, language, pitch, speed)
    create_word_files(tts, list_words, folder)
    retrieve_word_files(folder)


if __name__ == "__main__":
    main()
