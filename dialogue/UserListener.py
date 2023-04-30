import threading
import math

import config
from dialogue import HotWord, Speaker, Information
import time
import pyaudio
import wave
from datetime import datetime
import os
from threading import Timer

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

        self.running_seconds = -1
        self.processed_seconds = 0
        self.__start_listener_timer()

    def __start_listener_timer(self):
        self.running_seconds += 1
        if self.running:
            Timer(1, self.__start_listener_timer).start()

    def __detected_hotword(self):
        logger.debug("Hotword is detected.")
        self.__stop_listen_hotword()
        Speaker.play_sound("./dialogue/resources/where_to_go.mp3")
        self.listen()

    def __to_shorts(self, bytes):
        shorts = []
        for i in range(0, len(bytes), 2):
            n = bytes[i+1] * 256 + bytes[i]
            n = 32767 - n if n > 32767 else n
            shorts.append(n)
        return shorts

    def __input_audio(self, data):
        # 每二秒計算一次環境音
        if self.processed_seconds == self.running_seconds:
            return

        if self.running_seconds % 2 == 0:
            self.processed_seconds = self.running_seconds
            if not self.speaking and hasattr(config, 'env_noise'):
                # logger.debug("__input_audio data: %s" % (data[:50],))
                data = [x for x in self.__to_shorts(data) if x >= 0]                
                logger.debug("__input_audio data1: %s" % (data[:50],))
                audio_mean = sum([int(x) for x in data]) / len(data)
                config.env_noise = min(30, max(0, math.sqrt(audio_mean) // 2))
                logger.debug("__input_audio audio_mean: %f, env_noise: %d" % (audio_mean, config.env_noise))

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

        voice_data = []
        # print((RATE / chunk) * RECORD_SECONDS)
        head_voice_count = 0
        rear_silence_count = 0
        is_start_speaking = False
        chunk_count_per_second = RATE // chunk
        total_chunks = chunk_count_per_second * limit_seconds
        silence_count_threshold = chunk_count_per_second * 0.25
        wait_seconds = chunk / RATE * 0.95
        logger.debug("Total chunk: %d, Silence chunk: %f, Wait seconds: %f" % (total_chunks, silence_count_threshold, wait_seconds))
        if hasattr(config, 'env_noise'):
            env_noize = config.env_noise
        else:
            env_noize = 5
        logger.debug("env_noize: %s" % (env_noize,))
        for i in range(0, total_chunks):
            time.sleep(wait_seconds)
            try:
                buffer2 = audio_stream.read(chunk)
                buffer = bytearray([x if x > env_noize else 0 for x in buffer2])
                # print("buffer:", buffer)
            except Exception as ex:
                logger.error("Read audio stream error!\n%s", str(ex))
                break

            # Check silence 2
            zero_count = buffer.count(0)  # Get zero count in buffer
            if is_start_speaking:
                if zero_count < VOICE_THRESHOLD:
                    rear_silence_count = 0
                else:
                    rear_silence_count += 1
                if rear_silence_count > silence_count_threshold:
                    logger.debug("Stop voice, chunk_number = %d" % (i,))
                    break
            else:
                if zero_count < VOICE_THRESHOLD:
                    head_voice_count += 1
                else:
                    head_voice_count = 0
                if head_voice_count > 2:
                    is_start_speaking = True
                    logger.debug("Start voice, chunk_number = %d" % (i,))
            if zero_count < VOICE_THRESHOLD:
                voice_data.append(buffer)

        logger.debug("Done recording, chunk size: " + str(len(voice_data)))
        audio_stream.stop_stream()
        audio_stream.close()
        audio.terminate()

        # Write to file
        tag = datetime.now().strftime("%Y%m%d%H%M%S")
        output_filename_wave = "./dialogue/user/msg-" + tag + ".wav"
        wf = wave.open(output_filename_wave, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(voice_data))
        wf.close()
        logger.debug("Done wav writing: " + output_filename_wave)

        from pydub import AudioSegment
        song = AudioSegment.from_wav(output_filename_wave)
        output_filename_flac = "./dialogue/user/msg-" + tag + ".flac"
        song.export(output_filename_flac, format="flac")
        # os.remove(output_filename_wave)
        threading.Thread(target=lambda: os.remove(output_filename_wave)).start()
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
            HotWord.start_listen("./dialogue/resources/models/mei.pmdl",
                                 detected_callback=self.__detected_hotword,
                                 audio_input_callback=self.__input_audio)
            logger.info("End listening hot word")

    def run(self):
        self.listen_hotword()
        while self.running:
            if self.job_count > 0:
                Speaker.mute()
                Information.set_user_speaking(True)
                # try:
                self.__record(self.limit_seconds)
                # except Exception as ex:
                #     logger.error("Do record error!\n%s", str(ex))
                Information.set_user_speaking(False)
                Speaker.unmute()
                self.job_count = 0
                time.sleep(1)

            time.sleep(0.01)

        logger.info("terminated")

    def listen(self, limit_seconds=10):
        self.limit_seconds = limit_seconds
        self.job_count = 1

    def terminate(self):
        self.running = False
        HotWord.stop_listen()
        logger.warn("terminating")
