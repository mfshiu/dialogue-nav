from datetime import datetime
from playsound import playsound
import os
from dialogue import Information
from google.cloud import texttospeech
# import pygame

from dialogue.Helper import get_module_logger
import pyttsx3
# from Sub3 import sub3_play_sound

logger = get_module_logger(__name__)

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./dialogue//vin-gmsx-ad3eb9c8c7e6.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./dialogue//NCU-AI-3a285870a6aa.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./dialogue//NCU-AI-5e22fe333aae.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./dialogue/ncu-ai2-315510-1ea8beab4f1a.json"
# subprocess.check_call(['sqsub', '-np', sys.argv[1], '/path/to/executable'],
#                       env=dict(os.environ, SQSUB_VAR="visible in this subprocess"))

client = texttospeech.TextToSpeechClient()

global is_muted
is_muted = False

global _is_playing
_is_playing = False

voice = texttospeech.VoiceSelectionParams(
    language_code="zh-TW", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    speaking_rate=1.2,
    volume_gain_db=0.0
)

audio_config_quieter = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    speaking_rate=1.2,
    volume_gain_db=-1.5
)

def __generate_sound_file(audio_content, file_path=None):
    if file_path is None:
        tag = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = "./dialogue/output/speak-" + tag + ".mp3"
    with open(file_path, "wb") as out:
        # Write the response to the output file.
        out.write(audio_content)
        logger.debug('Audio content written to file: %s', file_path)

    return file_path


global __sound_message
__sound_message = None


def process_pyttsx3():
    global __sound_message

    if __sound_message:
        engine = pyttsx3.init()
        voice = engine.getProperty('voice')
        voices = engine.getProperty('voices')
        for item in voices:
            print(item.id, item.languages)
        engine.setProperty('voice', 'en')
        engine.say('Hello world')
        engine.say('123456')
        engine.runAndWait()
        __sound_message = None


def __do_play(msg, quieter=False):
    logger.debug("Speak: %s", msg)

    output_file = ""
    try:
        audio_content = __tts(msg, quieter)
        output_file = __generate_sound_file(audio_content)
        # output_file = 'file://' + pathname2url(os.path.abspath(output_file))
        __start_playing()

        playsound(output_file)
        # pygame.init()
        # pygame.mixer.init()
        # sound = pygame.mixer.Sound(output_file)
        # # sound.set_volume(0.5)  # Now plays at 90% of full volume.
        # sound.play()

        os.remove(output_file)
    except Exception as ex:
        logger.error("Play sound error, filename: %s, ex: %s", output_file, ex)
    finally:
        __stop_playing()


# def __do_play(msg):
#     logger.debug("Speak: %s", msg)
#
#     output_file = ""
#     try:
#         audio_content = __tts(msg)
#         output_file = __generate_sound_file(audio_content)
#         __start_playing()
#         playsound(output_file)
#         os.remove(output_file)
#     except Exception as ex:
#         logger.error("Play sound error, filename: %s, ex: %s", output_file, ex)
#     finally:
#         __stop_playing()


def __start_playing():
    Information.set_user_speaking(True)
    global _is_playing
    _is_playing = True


def __stop_playing():
    Information.set_user_speaking(False)
    global _is_playing
    _is_playing = False


def __tts(msg, quieter=False):
    synthesis_input = texttospeech.SynthesisInput(text=msg)
    config = audio_config_quieter if quieter else audio_config
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=config
    )
    return response.audio_content


def is_playing():
    return _is_playing


def mute():
    global is_muted
    is_muted = True


def unmute():
    global is_muted
    is_muted = False


def play(msg, quieter=False):
    if not is_muted:  # and not is_playing():
        __do_play(msg, quieter)
    return


def play_async(msg):
    play(msg)
    # if not is_muted:
    #     t = threading.Thread(target=__do_play, args=(msg,))
    #     t.start()
    # return


def play_sound(sound_file):
    logger.debug("Play sound: %s, is muted: %s", sound_file, is_muted)
    if not is_muted:
        __start_playing()
        playsound(sound_file)
        __stop_playing()


def save(msg, file_path):
    try:
        audio_content = __tts(msg)
        __generate_sound_file(audio_content, file_path)
    except:
        logger.debug("Save sound error: %s", file_path)
