def dm_encode(samples, step=1.0, start=0.0):
    """Delta modulation: 1 bit per sample (1 = step up, 0 = step down)."""
    staircase = start
    bits = []
    for x in samples:
        if x > staircase:       # analog signal is above the staircase
            bits.append(1)
            staircase += step
        else:                   # analog signal is at or below the staircase
            bits.append(0)
            staircase -= step
    return bits



def dm_decode(bits, step=1.0, start=0.0):
    """Rebuild the staircase signal from DM bits."""
    staircase = start
    levels = []
    for b in bits:
        if b == 1:
            staircase += step
        else:
            staircase -= step
        levels.append(staircase)
    return levels

if __name__ == "__main__":
    bits = dm_encode([2.0, 2.6, 3.4, 3.0], step=1.0)
    print(bits)                      # [1, 1, 1, 0]
    print(dm_decode(bits, step=1.0)) # should print [1.0, 2.0, 3.0, 2.0]