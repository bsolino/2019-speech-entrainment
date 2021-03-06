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
from pyaudio import PyAudio, paInt16, paComplete, paContinue
import wave
import numpy as np

THRESHOLD = 1400  # audio levels not normalised. # TODO Adjust value
#THRESHOLD = 640  # audio levels not normalised. # TODO Adjust value
#THRESHOLD = 170
RATE = 44100
CHUNK_SIZE = 1024
SILENT_CHUNKS = 1 * RATE // CHUNK_SIZE
FORMAT = paInt16
FRAME_MAX_VALUE = 2 ** 15 - 1
NORMALIZE_MINUS_ONE_dB = 10 ** (-1.0 / 20)
CHANNELS = 1
TRIM_APPEND = RATE / 4

THRESHOLD_REC = 10 # seconds




def find_threshold(rec_time = THRESHOLD_REC):
    p = PyAudio()
    stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK_SIZE
            )

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
            _to = min(len(data_all) - 1, len(data_all) - 1 - i + TRIM_APPEND)
#            _to = min(len(data_all) - 1, len(data_all) - 1 - i + TRIM_APPEND*2)  # Leave time for the sound to die
            break

    return copy.deepcopy(data_all[_from:(_to + 1)])


def record_automatic():
    """Record a word or words from the microphone and 
    return the data as an array of signed shorts."""

    p = PyAudio()
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


def record_semi_manual():
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.
    """

    stop = False
    data_all = array('h')
    def _callback_record(
            in_data,            # recorded data if input=True; else None
            frame_count,        # number of frames
            time_info,          # dictionary
            status_flags        # PaCallbackFlags:
            ):
        data_chunk = array('h', in_data)
        if byteorder == 'big':
            data_chunk.byteswap()
        data_all.extend(data_chunk)
        
        if stop:
            callback_flag = paComplete
        else:
            callback_flag = paContinue
        
        return in_data, callback_flag

    p = PyAudio()
    stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK_SIZE,
            stream_callback=_callback_record
            )

    stream.start_stream()
    
    raw_input("Press ENTER to stop recording")
    stop = True
    
#    while stream.is_active():
#        print("Still active")
#        sleep(0.01)


    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    data_all = trim(data_all)  # we trim before normalize as threshhold applies to un-normalized wave (as well as is_silent() function)
    
    data_all = normalize(data_all)
    return sample_width, data_all


def record_full_manual():
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.
    """
    
    raw_input("Press ENTER to START recording")
    stop = False
    data_all = array('h')
    def _callback_record(
            in_data,            # recorded data if input=True; else None
            frame_count,        # number of frames
            time_info,          # dictionary
            status_flags        # PaCallbackFlags:
            ):
        data_chunk = array('h', in_data)
        if byteorder == 'big':
            data_chunk.byteswap()
        data_all.extend(data_chunk)
        
        if stop:
            callback_flag = paComplete
        else:
            callback_flag = paContinue
        
        return in_data, callback_flag

    p = PyAudio()
    stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK_SIZE,
            stream_callback=_callback_record
            )

    stream.start_stream()
    
    raw_input("Press ENTER to stop recording")
    stop = True
    
#    while stream.is_active():
#        print("Still active")
#        sleep(0.01)


    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    data_all = trim(data_all)  # we trim before normalize as threshhold applies to un-normalized wave (as well as is_silent() function)
    
    data_all = normalize(data_all)
    return sample_width, data_all


def record_to_file(path, data, sample_width):
    "Records from the microphone and outputs the resulting data to 'path'"
    data = pack('<' + ('h' * len(data)), *data)

    wave_file = wave.open(path, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(sample_width)
    wave_file.setframerate(RATE)
    wave_file.writeframes(data)
    wave_file.close()


def play_file(path):
    # open the file for reading.
    wf = wave.open(path, 'rb')
    
    # create an audio object
    p = PyAudio()
    
    # open stream based on the wave object which has been input.
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)
    
    # read data (based on the chunk size)
    data = wf.readframes(CHUNK_SIZE)
    
    # play stream (looping from beginning of file to the end)
    while data != '':
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wf.readframes(CHUNK_SIZE)
    
    # cleanup stuff.
    stream.close()    
    p.terminate()

if __name__ == "__main__":
    find_threshold()