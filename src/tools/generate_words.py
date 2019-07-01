#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

#import paramiko
from nao_utils import create_proxy, IP, PORT
from word_list_utils import parse_file
# Voice configuration
from game_constants import PITCH_WORDS, SPEED_WORDS, LANG_EN
# NAO Folders
from game_constants import \
        NAO_FOLDER, WORDS_FOLDER_TEMPLATE, WORDS_FILE, GENERATION_FOLDER
from test_utils import TextToSpeechMock

LANG = LANG_EN

#FOLDER = "home/nao/entrainment/words"
#WORD_TYPE = "base"
PITCH = PITCH_WORDS
SPEED = SPEED_WORDS
DEST_FOLDER = NAO_FOLDER + GENERATION_FOLDER + WORDS_FOLDER_TEMPLATE.format(
        SPEED, PITCH)
TYPE_BASE = "base"
TYPE_SENTENCE = "sentence"

#FILE_TEMPLATE = "{}-{}-{}.wav"
FILE_TEMPLATE = "{}-{}.wav"


def configure_voice(tts, language, pitch, speed):
    """
    Prepare the voice to be used by the TTS system

    Default: All at 1. (no modifiers)
    """
    tts.setLanguage(language)
    tts.setParameter("pitchShift", pitch)
    tts.setParameter("speed", speed)
#    tts.setVoice(


def create_word_files(tts, data, dest_folder):
    """
    Use TTS to say the words to a file (internal in the robot)
    """
    for category in data.keys():
        for word_data in data[category]:
            if not word_data.is_sentence:
                word_type = TYPE_BASE
            else:
                word_type = TYPE_SENTENCE
            route = dest_folder + FILE_TEMPLATE.format(
#                    category, word_data.word, word_type)
                    word_data.word, word_type)
            print("Word " + word_data.word + "\tin route: " + route)
            tts.sayToFile(word_data.pronunciation, route)


def retrieve_word_files(dest_folder):
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
    dest_folder = DEST_FOLDER
    ip = IP
    port = PORT
    pitch = PITCH
    speed = SPEED
    language = LANG

    word_data = parse_file(filename)
    tts = create_proxy("ALTextToSpeech", ip, port)
#    tts = TextToSpeechMock
    configure_voice(tts, language, pitch, speed)
    create_word_files(tts, word_data.data, dest_folder)
    retrieve_word_files(dest_folder)


if __name__ == "__main__":
    main()
