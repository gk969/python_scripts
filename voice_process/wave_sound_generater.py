import numpy as np
import simpleaudio as sa
import matplotlib.pyplot as plt

f1 = 2000
f2 = 5
fs = 8000
seconds = 1

t = np.linspace(0, seconds, seconds * fs, False)

w1 = np.sin(f1 * t * 2 * np.pi)
w2 = np.sin(f2 * t * 2 * np.pi)

note = w1 * w2

# note = []
# print(len(w1))
# for i in range(len(w1)):
#     note.append(w1[i] * w2[i])

# audio = [int(value*32768) for value in note]

audio = note * (2**15 - 1) / np.max(np.abs(note))
audio = audio.astype(np.int16)

play_obj = sa.play_buffer(audio, 1, 2, fs)
play_obj.wait_done()

# ax = plt.subplot(211)
# plt.plot(note)

# ax = plt.subplot(212)
# plt.plot(audio)

# plt.show()
