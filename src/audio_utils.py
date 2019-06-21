# -*- coding: utf-8 -*-
#!/usr/bin/env python2
"""
Created on May  5 15:14:56 2013

@author: eugene
https://stackoverflow.com/questions/892199/detect-record-audio-in-python
https://stackoverflow.com/a/16385946

Note: Improved version over cryo's answer
"""


#Instead of adding silence at start and end of recording (values=0) I add the original audio . This makes audio sound more natural as volume is >0. See trim()
#I also fixed issue with the previous code - accumulated silence counter needs to be cleared once recording is resumed.

from array import array
from struct import pack
from sys import byteorder
import copy
import pyaudio
import wave
import numpy as np

THRESHOLD = 107  # audio levels not normalised. # TODO Adjust value
RATE = 44100
CHUNK_SIZE = 1024
SILENT_CHUNKS = 1 * RATE // CHUNK_SIZE
FORMAT = pyaudio.paInt16
FRAME_MAX_VALUE = 2 ** 15 - 1
NORMALIZE_MINUS_ONE_dB = 10 ** (-1.0 / 20)
CHANNELS = 1
TRIM_APPEND = RATE / 4


def find_threshold():
    p = pyaudio.PyAudio()
    stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK_SIZE
            )

    rec_time = 10  # seconds

    data_all = array('h')
    for i in range(0, RATE // CHUNK_SIZE * rec_time):
        # little endian, signed short
        data_chunk = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            data_chunk.byteswap()
        data_all.extend(data_chunk)

    max_data = array('h')
    for chunk in (range(
            len(data_all)//CHUNK_SIZE
            + 1*((len(data_all) % CHUNK_SIZE) > 0)
            )):
        _from = CHUNK_SIZE * chunk
        _to = min(len(data_all), CHUNK_SIZE * (chunk+1))
        max_data.append(max(data_all[_from:_to]))

#    mean = np.mean(np.abs(data_all))
#    std = np.std(np.abs(data_all))
#    threshold =  3 * std + mean
    mean = np.mean(max_data)
    std = np.std(max_data)
    threshold =  (3 * 3 * std) + mean
    
    print("AMP:\tmean: {:>4f}, std: {:>4f} , threshold: {:>4f}, rounded: {:>4f}".format(
            mean, std, threshold, np.round(threshold)
            ))
    

    stream.stop_stream()
    stream.close()
    p.terminate()
    
    return threshold


def is_silent(data_chunk):
    """Returns 'True' if below the 'silent' threshold"""
    print("{:>5d}: {}".format(max(data_chunk), max(data_chunk) < THRESHOLD))
    return max(data_chunk) < THRESHOLD


def normalize(data_all):
    """Amplify the volume out to max -1dB"""
    # MAXIMUM = 16384
    normalize_factor = (float(NORMALIZE_MINUS_ONE_dB * FRAME_MAX_VALUE)
                        / max(abs(i) for i in data_all))

    r = array('h')
    for i in data_all:
        r.append(int(i * normalize_factor))
    return r


def trim(data_all):
    _from = 0
    _to = len(data_all) - 1
    for i, b in enumerate(data_all):
        if abs(b) > THRESHOLD:
            _from = max(0, i - TRIM_APPEND)
            break

    for i, b in enumerate(reversed(data_all)):
        if abs(b) > THRESHOLD:
#            _to = min(len(data_all) - 1, len(data_all) - 1 - i + TRIM_APPEND)
            _to = min(len(data_all) - 1, len(data_all) - 1 - i + TRIM_APPEND*2)  # Leave time for the sound to die
            break

    return copy.deepcopy(data_all[_from:(_to + 1)])

def record():
    """Record a word or words from the microphone and 
    return the data as an array of signed shorts."""

    p = pyaudio.PyAudio()
    stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK_SIZE
            )

    silent_chunks = 0
    audio_started = False
    data_all = array('h')

    while True:
        # little endian, signed short
        data_chunk = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            data_chunk.byteswap()
        data_all.extend(data_chunk)

        silent = is_silent(data_chunk)

        if audio_started:
            if silent:
                silent_chunks += 1
                if silent_chunks > SILENT_CHUNKS:
                    break
            else: 
                silent_chunks = 0
        elif not silent:
            audio_started = True              

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    data_all = trim(data_all)  # we trim before normalize as threshhold applies to un-normalized wave (as well as is_silent() function)
    
    
    print("Total size: {}. N_Chunks: {}".format(
            len(data_all),
            len(data_all)/CHUNK_SIZE+1
            ))
    for chunk in (range(
            len(data_all)//CHUNK_SIZE
            + 1*((len(data_all) % CHUNK_SIZE) > 0)
            )):
        _from = CHUNK_SIZE * chunk
        _to = min(len(data_all), CHUNK_SIZE * (chunk+1))
        print("Chunk {:>3d}: max = {:>5d}".format(
                chunk, max(data_all[_from:_to])
                ))
    
    
    data_all = normalize(data_all)
    return sample_width, data_all

def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h' * len(data)), *data)

    wave_file = wave.open(path, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(sample_width)
    wave_file.setframerate(RATE)
    wave_file.writeframes(data)
    wave_file.close()

if __name__ == '__main__':
    print("Wait in silence to begin recording; wait in silence to terminate")
    record_to_file('demo.wav')
    print("done - result written to demo.wav")