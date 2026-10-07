def nrz_l_encode(bits):
    return [1 if b == 1 else -1 for b in bits]


def nrz_l_decode(signal):
    return [1 if v > 0 else 0 for v in signal]


def nrz_i_encode(bits):
    level = -1
    out = []
    for b in bits:
        if b == 1:
            level = -level
        out.append(level)
    return out


def nrz_i_decode(signal):
    prev = -1
    out = []
    for v in signal:
        out.append(1 if v != prev else 0)
        prev = v
    return out


def manchester_encode(bits):
    out = []
    for b in bits:
        if b == 1:
            out += [-1, 1]
        else:
            out += [1, -1]
    return out


def manchester_decode(signal):
    out = []
    for i in range(0, len(signal), 2):
        out.append(1 if signal[i] < signal[i + 1] else 0)
    return out


def diff_manchester_encode(bits):
    level = -1
    out = []
    for b in bits:
        if b == 0:
            level = -level      # 0: change at the start of the bit
        first = level
        level = -level          # change in the middle of every bit
        second = level
        out += [first, second]
    return out
 
 
def diff_manchester_decode(signal):
    prev = -1
    out = []
    for i in range(0, len(signal), 2):
        first = signal[i]
        out.append(1 if first == prev else 0)   # no change at start = 1
        prev = signal[i + 1]
    return out


 
def ami_encode(bits):
    last = -1               # so the first 1 becomes +1
    out = []
    for b in bits:
        if b == 1:
            last = -last    # 1s alternate between +1 and -1
            out.append(last)
        else:
            out.append(0)   # 0 is zero voltage
    return out
 
 
def ami_decode(signal):
    return [0 if v == 0 else 1 for v in signal]




def b8zs_encode(bits):
    last = -1                          # so the first 1 becomes +1
    out = []
    i = 0
    while i < len(bits):
        if bits[i:i + 8] == [0] * 8:   # eight zeros in a row
            if last == 1:
                out += [0, 0, 0, 1, -1, 0, -1, 1]
            else:
                out += [0, 0, 0, -1, 1, 0, 1, -1]
            i += 8                     # last pulse stays the same
        elif bits[i] == 1:
            last = -last               # normal AMI: 1s alternate
            out.append(last)
            i += 1
        else:
            out.append(0)
            i += 1
    return out
 
 
def b8zs_decode(signal):
    out = []
    i = 0
    while i < len(signal):
        chunk = signal[i:i + 8]
        if chunk == [0, 0, 0, 1, -1, 0, -1, 1] or chunk == [0, 0, 0, -1, 1, 0, 1, -1]:
            out += [0] * 8             # substitution pattern means 8 zeros
            i += 8
        else:
            out.append(0 if signal[i] == 0 else 1)
            i += 1
    return out
 

  
def hdb3_encode(bits):
    last = -1                          # so the first 1 becomes +1
    pulses = 0                         # pulses since the last substitution
    out = []
    i = 0
    while i < len(bits):
        if bits[i:i + 4] == [0] * 4:   # four zeros in a row
            if pulses % 2 == 1:        # odd number of pulses: 000V
                out += [0, 0, 0, last]
            else:                      # even number of pulses: B00V
                last = -last
                out += [last, 0, 0, last]
            pulses = 0
            i += 4
        elif bits[i] == 1:
            last = -last               # normal AMI: 1s alternate
            out.append(last)
            pulses += 1
            i += 1
        else:
            out.append(0)
            i += 1
    return out
 
 
def hdb3_decode(signal):
    out = []
    last = -1
    for v in signal:
        if v == 0:
            out.append(0)
        elif v == last:                # same polarity twice: this is a V
            out[-3:] = [0, 0, 0]       # the four values were really 0000
            out.append(0)
        else:
            out.append(1)
            last = v
    return out