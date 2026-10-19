import math
import matplotlib.pyplot as plt


def pcm_encode(samples, n_bits=3, v_min=-1.0, v_max=1.0):
    """Pulse code modulation: each sample becomes n_bits bits.

    1. Sampling      - already done, `samples` are the sampled values.
    2. Quantization  - round each sample to the nearest of 2**n_bits levels.
    3. Encoding      - write the level number in binary (MSB first).
    """
    num_levels = 2 ** n_bits
    step = (v_max - v_min) / (num_levels - 1)   # gap between two levels
    bits = []
    for x in samples:
        index = round((x - v_min) / step)       # quantization
        index = max(0, min(num_levels - 1, index))  # clamp if x is out of range
        for i in range(n_bits - 1, -1, -1):     # encoding, MSB first
            bits.append((index >> i) & 1)
    return bits


def pcm_decode(bits, n_bits=3, v_min=-1.0, v_max=1.0):
    """Rebuild the quantized (staircase) signal from PCM bits."""
    num_levels = 2 ** n_bits
    step = (v_max - v_min) / (num_levels - 1)
    levels = []
    for start in range(0, len(bits), n_bits):
        index = 0
        for b in bits[start:start + n_bits]:    # binary -> level number
            index = index * 2 + b
        levels.append(v_min + index * step)     # level number -> voltage
    return levels


if __name__ == "__main__":
    # analog input: one cycle of a sine wave, 40 samples
    amplitude = 3
    samples = [amplitude * math.sin(2 * math.pi * k / 40) for k in range(40)]
    n_bits = 3   # try 2 and 4: more bits = finer levels = less quantization error

    bits = pcm_encode(samples, n_bits=n_bits, v_min=-amplitude, v_max=amplitude)
    levels = pcm_decode(bits, n_bits=n_bits, v_min=-amplitude, v_max=amplitude)

    print("PCM bits:", "".join(map(str, bits)))

    plt.figure(figsize=(10, 4))
    plt.plot(samples, label="Analog signal")
    plt.step(range(len(levels)), levels, where="mid", label="PCM quantized signal")
    plt.legend()
    plt.title("Pulse code modulation")
    plt.show()