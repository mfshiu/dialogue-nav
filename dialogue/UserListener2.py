import threading
from dialogue import Speaker
import time
import pyaudio
import wave
from datetime import datetime
import os

from dialogue.Helper import get_module_logger
logger = get_module_logger(__name__)

CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
VOICE_THRESHOLD = 500


class UserListener2(threading.Thread):

    def __init__(self, args=()):
        super(UserListener2, self).__init__()
        logger.debug("__init__")

        self.running = True
        self.speaking = False
        self.user_words = args[0]

    def __record(self):
        logger.info("---recording---")
        self.speaking = False

        audio = pyaudio.PyAudio()
        audio_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                                  input=True, frames_per_buffer=CHUNK_SIZE)
        sample_size = audio.get_sample_size(FORMAT)
        voice_data = []
        head_voice_count = 0
        rear_zero_count = 0
        is_start_speaking = False
        silence_count = RATE // CHUNK_SIZE * 0.25
        i = -1
        while not Speaker.is_playing():
            i += 1
            if i > 1000 and not is_start_speaking:
                logger.debug("Quit recording.")
                break
            time.sleep(0.03)
            chunk_data = audio_stream.read(CHUNK_SIZE)

            zero_cnt = chunk_data.count(0)
            if is_start_speaking:
                if zero_cnt < VOICE_THRESHOLD:
                    rear_zero_count = 0
                else:
                    rear_zero_count += 1
                if rear_zero_count > silence_count:
                    self.speaking = False
                    logger.debug("Stop voice, i = " + str(i))
                    break
            else:
                if zero_cnt < VOICE_THRESHOLD:
                    head_voice_count += 1
                else:
                    head_voice_count = 0
                if head_voice_count > 2:
                    is_start_speaking = True
                    self.speaking = True
                    logger.debug("Start voice, i = " + str(i))
            if zero_cnt < VOICE_THRESHOLD:
                voice_data.append(chunk_data)
                if len(voice_data) > 100:
                    break
                # logger.debug("len(voice_data): %d", len(voice_data))

        audio_stream.stop_stream()
        audio_stream.close()
        audio.terminate()

        logger.debug("Done recording, chunk size: " + str(len(voice_data)))
        if len(voice_data) > 0:
            output_filename_flac = self.write_to_flac(voice_data, sample_size)
            self.user_words.put(output_filename_flac)
            # Speaker.play_sound(output_filename_flac)

    def write_to_flac(self, voice_data, sample_size):
        # Write to wave file
        tag = datetime.now().strftime("%Y%m%d%H%M%S")
        output_filename_wave = "./dialogue/user/msg-" + tag + ".wav"
        wf = wave.open(output_filename_wave, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(sample_size)
        wf.setframerate(RATE)
        wf.writeframes(b''.join(voice_data))
        wf.close()
        logger.debug("Done wav writing: " + output_filename_wave)

        # Convert to flac
        output_filename_flac = "./dialogue/user/msg-" + tag + ".flac"
        from pydub import AudioSegment
        song = AudioSegment.from_wav(output_filename_wave)
        song.export(output_filename_flac, format="flac")
        os.remove(output_filename_wave)
        logger.debug("Done flac writing: " + output_filename_wave)

        return output_filename_flac

    def run(self):
        while self.running:
            if not Speaker.is_playing():
                self.__record()
            time.sleep(0.1)
        logger.info("terminated")

    def terminate(self):
        self.running = False
        logger.warn("terminating")


if __name__ == '__main__':
    import queue
    user_words = queue.Queue(10)
    user_listener = UserListener2(args=(user_words,))
    user_listener.start()
