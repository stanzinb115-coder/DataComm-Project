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

 