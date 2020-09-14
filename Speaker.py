from datetime import datetime
from playsound import playsound
import os
import threading
# import subprocess
# import sys

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./NCU-AI-5e22fe333aae.json" # visible in this process + all children
# subprocess.check_call(['sqsub', '-np', sys.argv[1], '/path/to/executable'],
#                       env=dict(os.environ, SQSUB_VAR="visible in this subprocess"))
from google.cloud import texttospeech


client = texttospeech.TextToSpeechClient()

voice = texttospeech.VoiceSelectionParams(
    language_code="zh-TW", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)


def __do_play(msg):
    print("Speaker: " + msg)
    synthesis_input = texttospeech.SynthesisInput(text=msg)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    tag = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = "./output/speak-" + tag + ".mp3"
    with open(output_file, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file: ' + output_file)

    playsound(output_file)
    os.remove(output_file)


def play(msg):
    __do_play(msg)
    return


def play_async(msg):
    t = threading.Thread(target=__do_play, args=(msg,))
    t.start()
    return


def play_sound(sound_file):
    playsound(sound_file)
