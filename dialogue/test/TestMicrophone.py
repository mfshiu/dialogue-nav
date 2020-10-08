import pyaudio
import wave


chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "../resources/a_test_2.wav"

p = pyaudio.PyAudio()

# Création et initialisation de l'objet stream...
s = p.open(format = FORMAT,
 channels = CHANNELS,
 rate = RATE,
 input = True,
 frames_per_buffer = chunk)

print("---recording---")

d = []

print((RATE/chunk) * RECORD_SECONDS)

for i in range(0, (RATE//chunk * RECORD_SECONDS)):

 data = s.read(chunk)
 d.append(data)
 #s.write(data, chunk)

print("---done recording---")

s.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(d))
wf.close()