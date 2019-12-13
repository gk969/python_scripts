import numpy as np
import simpleaudio as sa
import matplotlib.pyplot as plt

CYCLES = 20
SAMPLE_RATE = 32000
TONE_SETS=[697, 770, 852, 941, 1209, 1336, 1477, 1633]

sine_sets=[]
cut_sine_sets=[]
for tone in TONE_SETS:
    sample_num=(int)(CYCLES*SAMPLE_RATE/tone);
    t=np.linspace(0, sample_num*tone/SAMPLE_RATE, sample_num, False)
    wave=np.sin(t * 2 * np.pi)
    sine_sets.append(wave)
    
    for i in range(0, len(wave)):
        if i>(5*SAMPLE_RATE/tone):
            if abs(wave[i])<0.01 and wave[i-1]<0:
                print("tone %d full %d cut %d %f %f" % (tone, len(wave), i, wave[i-1], wave[len(wave)-1]))
                wave=wave[0:i]
                break
    cut_sine_sets.append(wave)

with open("dtmf_wave.h", "wt") as out:
    for i in range(0, len(TONE_SETS)):
        wave_str=""
        
        wave=cut_sine_sets[i]
        for h in range(0, len(wave)):
            value=int((wave[h]+1)*1023)
            wave_str+="0x%04X, " % value
            if (h+1)%4 == 0:
                wave_str+=" "
            if (h+1)%8 == 0:
                wave_str+="\n"
        
        print("const u16 WAVE_SINE_%d[%d] = {\n%s\n};" % (TONE_SETS[i], len(cut_sine_sets[i]), wave_str[0:-2]), file=out)
    

ax = plt.subplot(221)
ax.grid(True, linestyle='-')
plt.plot(sine_sets[0], 'r-o')

ax = plt.subplot(222)
ax.grid(True, linestyle='-')
plt.plot(sine_sets[7], 'r-o')

ax = plt.subplot(223)
ax.grid(True, linestyle='-')
plt.plot(cut_sine_sets[0], 'r-o')

ax = plt.subplot(224)
ax.grid(True, linestyle='-')
plt.plot(cut_sine_sets[7], 'r-o')

plt.show()
