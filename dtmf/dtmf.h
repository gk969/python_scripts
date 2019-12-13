#include "dtmf_wave.h"

#pragma pack(1)
typedef struct{
    const u16* wave;
    u16 len;
}Wave_sine;
#pragma pack()

const Wave_sine DTMF_SINE[] = {
    {WAVE_SINE_697, sizeof(WAVE_SINE_697)/sizeof(u16)},
    {WAVE_SINE_770, sizeof(WAVE_SINE_770)/sizeof(u16)},
    {WAVE_SINE_852, sizeof(WAVE_SINE_852)/sizeof(u16)},
    {WAVE_SINE_941, sizeof(WAVE_SINE_941)/sizeof(u16)},
    {WAVE_SINE_1209, sizeof(WAVE_SINE_1209)/sizeof(u16)},
    {WAVE_SINE_1336, sizeof(WAVE_SINE_1336)/sizeof(u16)},
    {WAVE_SINE_1477, sizeof(WAVE_SINE_1477)/sizeof(u16)},
    {WAVE_SINE_1633, sizeof(WAVE_SINE_1633)/sizeof(u16)},
};

enum{
    WAVE_697=0, 
    WAVE_770, 
    WAVE_852, 
    WAVE_941, 
    WAVE_1209,
    WAVE_1336,
    WAVE_1477,
    WAVE_1633,
};

const u8 DTMF_NUM[16][2] = {
    {WAVE_941, WAVE_1336},
    {WAVE_697, WAVE_1209},
    {WAVE_697, WAVE_1336},
    {WAVE_697, WAVE_1477},
    
    {WAVE_770, WAVE_1209},
    {WAVE_770, WAVE_1336},
    {WAVE_770, WAVE_1477},
    {WAVE_852, WAVE_1209},
    
    {WAVE_852, WAVE_1336},
    {WAVE_852, WAVE_1477},
    {WAVE_941, WAVE_1336},
    {WAVE_941, WAVE_1209},
    
    {WAVE_941, WAVE_1477},
    {WAVE_697, WAVE_1633},
    {WAVE_770, WAVE_1633},
    {WAVE_852, WAVE_1633},
};