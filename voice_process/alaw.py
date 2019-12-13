seg_end = (0xFF, 0x1FF, 0x3FF, 0x7FF, 0xFFF, 0x1FFF, 0x3FFF, 0x7FFF)
SIGN_BIT=0x80
QUANT_MASK=0xf
SEG_SHIFT=4
SEG_MASK=0x70

def search(val, size) :
    for i in range(size):
        if (val <= seg_end[i]):
            return i
    return size


def linear_to_alaw(pcm_val):
    if (pcm_val >= 0):
        mask = 0xD5
    else:
        mask = 0x55
        pcm_val = -pcm_val - 8
    
    seg = search(pcm_val, 8)

    if (seg >= 8) :
        return (0x7F ^ mask)

    aval = seg << SEG_SHIFT
    if (seg < 2):
        aval |= (pcm_val >> 4) & QUANT_MASK
    else:
        aval |= (pcm_val >> (seg + 3)) & QUANT_MASK
    return (aval ^ mask)

def alaw_to_linnear(a_val):
    a_val ^= 0x55

    t = (a_val & QUANT_MASK) << 4
    seg = (a_val & SEG_MASK) >> SEG_SHIFT
    if seg == 0:
        t += 8
    elif seg == 1:
        t += 0x108
    else:
        t += 0x108
        t <<= seg - 1
    
    if (a_val & SIGN_BIT)!=0: 
        return t
    else:
        return -t
