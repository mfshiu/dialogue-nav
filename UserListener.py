import threading
import HotWord
import Speaker
import time
import pyaudio
import wave
import random
from datetime import datetime
import os
import subprocess

from Helper import get_module_logger
logger = get_module_logger(__name__)


chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # 44100
# RECORD_SECONDS = 5
# WAVE_OUTPUT_FILENAME = "resources/user_speak.wav"


class UserListener(threading.Thread):

    def __init__(self, group=None, args=(), kwargs=None, verbose=None):
        super(UserListener, self).__init__()
        self.limit_seconds = 5
        self.running = True
        self.starting = False
        self.recording = False
        self.job_count = 0
        self.user_words = args[0]
        self.audio = pyaudio.PyAudio()
        logger.debug("__init__")

    def __record(self):
        logger.info("---recording---")
        # self.audio = pyaudio.PyAudio()
        audio_stream = self.audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=chunk)
        d = []
        # print((RATE / chunk) * RECORD_SECONDS)
        for i in range(0, (RATE // chunk * self.limit_seconds)):
            data = audio_stream.read(chunk)
            d.append(data)
            # audio_stream.write(data, chunk)
        logger.debug("Done recording")

        # audio_stream.close()
        self.audio.close(audio_stream)
        # self.audio.terminate()

        # Write to file
        tag = datetime.now().strftime("%Y%m%d%H%M%S")
        output_filename_wave = "user/msg-" + tag + ".wav"
        output_filename_flac = "user/msg-" + tag + ".flac"
        wf = wave.open(output_filename_wave, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(d))
        wf.close()
        logger.debug("Done wav writing: " + output_filename_wave)

        from pydub import AudioSegment
        song = AudioSegment.from_wav(output_filename_wave)
        song.export(output_filename_flac, format="flac")
        os.remove(output_filename_wave)
        self.user_words.put(output_filename_flac)
        logger.debug("Done flac writing: " + output_filename_wave)

        # # Convert wav to mp3
        # cmd = 'lame --preset insane %s' % wave_output_filename
        # subprocess.call(cmd, shell=True)
        # os.remove(wave_output_filename)
        # # Add user words
        # self.user_words.put(mp3_output_filename)

    def run(self):
        while self.running:
            if self.job_count > 0:
                self.__record()
                self.job_count -= 1
                time.sleep(1)
            time.sleep(0.1)
        logger.info("terminated")

    def start_record(self, limit_seconds=5):
        self.limit_seconds = limit_seconds
        self.job_count += 1

    def terminate(self):
        self.running = False
        self.audio.terminate()
        logger.warn("terminating")
