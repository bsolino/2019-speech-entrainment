#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

#import paramiko
from nao_utils import create_proxy, IP, PORT
from word_list_utils import parse_file, WORDS_FILE

PITCH = 1
SPEED = .75 * 100
LANG = "English"

#FOLDER = "home/nao/entrainment/words"
#WORD_TYPE = "base"
FOLDER = "home/nao/entrainment/words/practice"
WORD_TYPE = "practice"
WORDS_FILE = "data/list_practice_words.txt"


def configure_voice(tts, language, pitch, speed):
    """
    Prepare the voice to be used by the TTS system

    Default: All at 1. (no modifiers)
    """
    tts.setLanguage(language)
    tts.setParameter("pitchShift", pitch)
    tts.setParameter("speed", speed)
#    tts.setVoice(


def create_word_files(tts, data, folder):
    """
    Use TTS to say the words to a file (internal in the robot)
    """
    for category in data.keys():
        for word_data in data[category]:
            route = "/" + folder + "/" \
                    + category + "-" + word_data.word + "-" + WORD_TYPE + ".wav"
            print("Word " + word_data.word + "\tin route: " + route)
            tts.sayToFile(word_data.pronunciation, route)


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
    filename = WORDS_FILE
    folder = FOLDER
    ip = IP
    port = PORT
    pitch = PITCH
    speed = SPEED
    language = LANG

    word_data = parse_file(filename)
    tts = create_proxy("ALTextToSpeech", ip, port)
    configure_voice(tts, language, pitch, speed)
    create_word_files(tts, word_data.data, folder)
    retrieve_word_files(folder)


if __name__ == "__main__":
    main()