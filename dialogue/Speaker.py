from datetime import datetime
from playsound import playsound
import os
import threading
from dialogue import Information

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./dialogue//NCU-AI-5e22fe333aae.json" # visible in this process + all children
# subprocess.check_call(['sqsub', '-np', sys.argv[1], '/path/to/executable'],
#                       env=dict(os.environ, SQSUB_VAR="visible in this subprocess"))
from google.cloud import texttospeech


client = texttospeech.TextToSpeechClient()

global is_muted
is_muted = False

voice = texttospeech.VoiceSelectionParams(
    language_code="zh-TW", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    speaking_rate=1.2
)


def __generate_sound_file(audio_content, file_path=None):
    if file_path is None:
        tag = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = "./dialogue/output/speak-" + tag + ".mp3"
    with open(file_path, "wb") as out:
        # Write the response to the output file.
        out.write(audio_content)
        print('Audio content written to file: ' + file_path)

    return file_path


def __do_play(msg):
    print("Speak: " + msg)

    output_file = ""
    try:
        audio_content = __tts(msg)
        output_file = __generate_sound_file(audio_content)
        Information.set_user_speaking(True)
        playsound(output_file)
        os.remove(output_file)
    except:
        print("Play sound error: ", output_file)
    finally:
        Information.set_user_speaking(False)


def __tts(msg):
    synthesis_input = texttospeech.SynthesisInput(text=msg)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content


def mute():
    global is_muted
    is_muted = True


def unmute():
    global is_muted
    is_muted = False


def play(msg):
    if not is_muted:
        __do_play(msg)
    return


def play_async(msg):
    if not is_muted:
        t = threading.Thread(target=__do_play, args=(msg,))
        t.start()
    return


def play_sound(sound_file):
    if not is_muted:
        Information.set_user_speaking(True)
        playsound(sound_file)
        Information.set_user_speaking(False)


def save(msg, file_path):
    try:
        audio_content = __tts(msg)
        __generate_sound_file(audio_content, file_path)
    except:
        print("Save sound error: ", file_path)
