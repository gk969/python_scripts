import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import sys
import base64
import alaw

FS=8000

def wav_show(wave_data):
    time = np.arange(0, len(wave_data)) * (1.0/FS)
    plt.plot(time, wave_data)
    plt.show()


def read_voice_text(txt_file):
    voice_name = []
    with open(txt_file, 'rt') as txt:
        for line in txt:
            line = line.replace("\n", "")
            words = list(filter(None, line.split(" ")))
            voice_name.append(words)
    return voice_name


def voice_activity_detect(raw_wave):
    voice_wave = []
    wave_fragment = []
    MAX_IDLE_SAMPLE = 0.1*FS
    MIN_VALID_LEN = 0.05*FS
    VALID_THRESHOLD=48
    idle_sample = 0
    first_idle_index = 0
    for sample in raw_wave:
        if(abs(sample) > VALID_THRESHOLD):
            wave_fragment.append(sample)
            idle_sample = 0
        else:
            if(idle_sample < MAX_IDLE_SAMPLE):
                if len(wave_fragment)!=0:
                    wave_fragment.append(sample)
                if(idle_sample == 0):
                    first_idle_index = len(wave_fragment)
                idle_sample += 1
                if(idle_sample >= MAX_IDLE_SAMPLE and first_idle_index != 0):
                    wave_fragment = wave_fragment[:first_idle_index+1]
                    if len(wave_fragment) > MIN_VALID_LEN:
                        voice_wave.append(wave_fragment)
                    wave_fragment = []
                    first_idle_index = 0

    if(len(wave_fragment) != 0):
        if(idle_sample != 0):
            wave_fragment = wave_fragment[:first_idle_index+1]
        voice_wave.append(wave_fragment)

    return voice_wave

def read_wave(wav_file):
    fs, raw_wave = wavfile.read(wav_file)
    if fs!=FS:
        sys.exit("fs %d Error" % fs)
    return raw_wave

def read_voice_wave(voice_dir, voice_name):
    voice_list=[]
    for name in voice_name:
        raw_wave = read_wave(voice_dir+"/"+name+".wav")
        voice_wave = voice_activity_detect(raw_wave)
        if len(voice_wave)!=1:
            sys.exit("voice %s detect error" % name)
        voice_list.append(voice_wave[0])

    return voice_list


def write_cmd_style_alaw_wave(voice_name, voice_wave, out_file):
    with open(out_file, "wt") as out:
        name_str=""
        for name in voice_name:
            name_str += "\"%s\":\"%s\"," % (name[1], name[0])
        print("voice_name {%s}" % name_str[0:-1], file=out)

        list_str = ""
        chksum=0
        total_len=0
        wave_all=[]
        for wave in voice_wave:
            offset=total_len
            wave_len = len(wave)
            chksum += offset+wave_len
            list_str += "%08X_%08X," % (offset, wave_len)
            total_len += len(wave)
            wave_all+=[(alaw.linear_to_alaw(value)) for value in wave]
        chksum+=total_len
        print("voice_list chksum:%08X,total:%08X,list:%s" % (chksum, total_len, list_str), file=out)
        print("voice_list voice %d samples %d" % (len(voice_wave), total_len))

        PACK_SIZE_MAX=512
        offset=0
        for pack_offset in range(0, len(wave_all), PACK_SIZE_MAX):
            pack_size=len(wave_all)-pack_offset
            if pack_size>PACK_SIZE_MAX:
                pack_size=PACK_SIZE_MAX
            
            chksum=0
            pack=wave_all[pack_offset:pack_offset+pack_size]
            for value in pack:
                chksum+=value
            chksum += offset+pack_size
            wave_str = base64.b64encode(bytes(pack)).decode("ascii")
            print("voice_wave chksum:%08X,offset:%08X,len:%04X,data:%s" % (chksum, offset, pack_size, wave_str), file=out)

            offset += pack_size


if(__name__ == '__main__'):
    voice_name = read_voice_text("voice.txt")
    # print(voice_name)

    voice_wave = read_voice_wave("female_voice", [name[1] for name in voice_name])

    alarm_horn_wave = read_wave("horn_shorter_single.wav")
    # alarm_horn_wave = read_wave("alarm_horn_single.wav")
    # wav_show(alarm_horn_wave)

    voice_name.append(["警号声", "alarm_horn"])
    voice_wave.append(alarm_horn_wave)

    if len(voice_name) != len(voice_wave):
        print("len(voice_name) != len(voice_wave) ERROR !!!")
        exit()

    # wav_show(voice_wave[0])
    # for wave in voice_wave:
        # wav_show(wave)

    write_cmd_style_alaw_wave(voice_name, voice_wave, "female.cwv")
