import threading
from dialogue import HotWord, Speaker
import time
import pyaudio
import wave
from datetime import datetime
import os

from dialogue.Helper import get_module_logger
logger = get_module_logger(__name__)


chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # 44100
VOICE_THRESHOLD = 500
# RECORD_SECONDS = 5
# WAVE_OUTPUT_FILENAME = "resources/user_speak.wav"


class UserListener(threading.Thread):

    def __init__(self, group=None, args=(), kwargs=None, verbose=None):
        super(UserListener, self).__init__()
        logger.debug("__init__")

        self.limit_seconds = 10
        self.running = True
        self.speaking = False
        self.job_count = 0
        self.user_words = args[0]

    def __detected_hotword(self):
        logger.debug("__detected_hotword")
        self.__stop_listen_hotword()
        Speaker.play_sound("./dialogue/resources/where_to_go.mp3")
        self.listen()

    def __stop_listen_hotword(self):
        logger.info("Stop listen hot word")
        HotWord.stop_listen()

    def __record(self, limit_seconds):
        self.speaking = True
        logger.info("---recording---")

        while HotWord.is_listening():
            self.__stop_listen_hotword()
            logger.warn("Waiting hot word stop.")
            time.sleep(1)

        audio = pyaudio.PyAudio()
        audio_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                                       input=True, frames_per_buffer=chunk)

        d = []
        # print((RATE / chunk) * RECORD_SECONDS)
        head_voice_count = 0
        rear_zero_count = 0
        is_start_speaking = False
        total = RATE // chunk * limit_seconds
        silence_count = RATE // chunk * 0.25
        logger.debug("Total chunk: " + str(total) + ", Silence chunk: " + str(silence_count))
        for i in range(0, total):
            data = audio_stream.read(chunk)

            # Check silence
            cnt = data.count(0)
            if is_start_speaking:
                if cnt < VOICE_THRESHOLD:
                    rear_zero_count = 0
                else:
                    rear_zero_count += 1
                if rear_zero_count > silence_count:
                    logger.debug("Stop voice, i = " + str(i))
                    break
            else:
                if cnt < VOICE_THRESHOLD:
                    head_voice_count += 1
                else:
                    head_voice_count = 0
                if head_voice_count > 2:
                    is_start_speaking = True
                    logger.debug("Start voice, i = " + str(i))
            if cnt < VOICE_THRESHOLD:
                d.append(data)

        logger.debug("Done recording, chunk size: " + str(len(d)))
        audio_stream.stop_stream()
        audio_stream.close()
        audio.terminate()

        # Write to file
        tag = datetime.now().strftime("%Y%m%d%H%M%S")
        output_filename_wave = "./dialogue/user/msg-" + tag + ".wav"
        output_filename_flac = "./dialogue/user/msg-" + tag + ".flac"
        wf = wave.open(output_filename_wave, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
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

        self.speaking = False

    def listen_hotword(self):
        if HotWord.is_listening():
            logger.warn("HotWord is listening.")
        elif self.speaking:
            logger.warn("User is speaking.")
        else:
            logger.info("Begin listening hot word")
            HotWord.start_listen("./dialogue/resources/models/mei.pmdl", self.__detected_hotword)
            logger.info("End listening hot word")

    def run(self):
        self.listen_hotword()
        while self.running:
            if self.job_count > 0:
                Speaker.mute()
                self.__record(self.limit_seconds)
                Speaker.unmute()
                self.job_count = 0
                time.sleep(1)
            time.sleep(0.1)
        logger.info("terminated")

    def listen(self, limit_seconds=10):
        self.limit_seconds = limit_seconds
        self.job_count = 1

    def terminate(self):
        self.running = False
        HotWord.stop_listen()
        logger.warn("terminating")
