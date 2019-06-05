#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

#import paramiko
from nao_utils import create_proxy, IP, PORT
from word_list_utils import parse_file

PITCH = 1
SPEED = .75 * 100
LANG = "English"

FILENAME = "list_words.txt"
FOLDER = "home/nao/entrainment/words"


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
        route = "/" + folder + "/" + word + "-base."
        print("Word " + word + "\tin route: " + route)
#        tts.sayToFile(word, route + "raw")
        tts.sayToFile(word, route + "wav")


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
    filename = FILENAME
    folder = FOLDER
    ip = IP
    port = PORT
    pitch = PITCH
    speed = SPEED
    language = LANG

    list_words = parse_file(filename).get_all_words()
    print(list_words)
    tts = create_proxy("ALTextToSpeech", ip, port)
    configure_voice(tts, language, pitch, speed)
    create_word_files(tts, list_words, folder)
    retrieve_word_files(folder)


if __name__ == "__main__":
    main()
