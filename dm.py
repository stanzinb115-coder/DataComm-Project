import math
import matplotlib.pyplot as plt

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
    # analog input: one cycle of a sine wave, 40 samples
    samples = [3 * math.sin(2 * math.pi * k / 40) for k in range(40)]
    step = 0.5
# (with step=0.2 and0.1)This is the main trade-off in DM,: a small step lags on steep parts, a big step is rough on flat parts.
    bits = dm_encode(samples, step=step)
    levels = dm_decode(bits, step=step)

    print("DM bits:", "".join(map(str, bits)))

    plt.figure(figsize=(10, 4))
    plt.plot(samples, label="Analog signal")
    plt.step(range(len(levels)), levels, where="post", label="DM staircase")
    plt.legend()
    plt.title("Delta modulation")
    plt.show()