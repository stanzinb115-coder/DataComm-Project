import matplotlib.pyplot as plt
import math
from dm import dm_encode, dm_decode
from pcm import pcm_encode, pcm_decode
from generator import generate_random, generate_with_zero_runs, longest_palindrome
from encoders import (
    nrz_l_encode, nrz_l_decode,
    nrz_i_encode, nrz_i_decode,
    manchester_encode, manchester_decode,
    diff_manchester_encode, diff_manchester_decode,
    ami_encode, ami_decode,
    b8zs_encode, b8zs_decode,
    hdb3_encode, hdb3_decode,
)

LINE_CODES = {
    "1": ("NRZ-L", nrz_l_encode, nrz_l_decode),
    "2": ("NRZ-I", nrz_i_encode, nrz_i_decode),
    "3": ("Manchester", manchester_encode, manchester_decode),
    "4": ("Differential Manchester", diff_manchester_encode, diff_manchester_decode),
    "5": ("AMI", ami_encode, ami_decode),
}

SCRAMBLING = {
    "1": ("B8ZS", b8zs_encode, b8zs_decode),
    "2": ("HDB3", hdb3_encode, hdb3_decode),
}


def get_digital_data():
    n = int(input("How many bits? "))
    kind = input("Random data (1) or data with zero runs (2)? ").strip()

    if kind == "2":
        run_length = int(input("Run length (4 or 8)? "))
        return generate_with_zero_runs(n, run_length=run_length, num_runs=2)
    return generate_random(n)


def choose_line_code():
    print("Line codes:")
    for key, (name, _, _) in LINE_CODES.items():
        print(f"  {key}. {name}")
    name, encode, decode = LINE_CODES[input("Choose: ").strip()]

    if name == "AMI":
        if input("Scrambling needed? (y/n) ").strip().lower() == "y":
            print("Scrambling types:")
            for key, (sname, _, _) in SCRAMBLING.items():
                print(f"  {key}. {sname}")
            name, encode, decode = SCRAMBLING[input("Choose: ").strip()]

    return name, encode, decode


def plot_signal(signal, title):
    levels = signal + [signal[-1]]   # repeat last level so the last bit is drawn fully
    plt.figure(figsize=(12, 3))
    plt.step(range(len(levels)), levels, where="post")
    plt.ylim(-2, 2)
    plt.title(title)
    plt.show()


def get_dm_bits():
    amplitude = float(input("Amplitude of the sine wave (for example 3)? "))
    n = int(input("Number of samples (for example 40)? "))
    step = float(input("DM step size (for example 0.5)? "))

    samples = [amplitude * math.sin(2 * math.pi * k / n) for k in range(n)]
    bits = dm_encode(samples, step=step)
    levels = dm_decode(bits, step=step)

    plt.figure(figsize=(10, 4))
    plt.plot(samples, label="Analog signal")
    plt.step(range(len(levels)), levels, where="post", label="DM staircase")
    plt.legend()
    plt.title("Delta modulation")
    plt.show()
    return bits


def get_pcm_bits():
    amplitude = float(input("Amplitude of the sine wave (for example 3)? "))
    n = int(input("Number of samples (for example 40)? "))
    n_bits = int(input("Bits per sample (for example 3)? "))

    samples = [amplitude * math.sin(2 * math.pi * k / n) for k in range(n)]
    bits = pcm_encode(samples, n_bits, -amplitude, amplitude)
    levels = pcm_decode(bits, n_bits, -amplitude, amplitude)

    plt.figure(figsize=(10, 4))
    plt.plot(samples, label="Analog signal")
    plt.step(range(len(levels)), levels, where="mid", label="PCM quantized signal")
    plt.legend()
    plt.title("Pulse code modulation")
    plt.show()
    return bits


ANALOG_MODES = {
    "1": get_pcm_bits,
    "2": get_dm_bits,
}


def get_analog_bits():
    choice = input("PCM (1) or DM (2)? ").strip()
    return ANALOG_MODES[choice]()


INPUT_TYPES = {
    "1": get_digital_data,
    "2": get_analog_bits,
}


def get_input_bits():
    choice = input("Digital input (1) or analog input (2)? ").strip()
    return INPUT_TYPES[choice]()


def main():
    bits = get_input_bits()
    print("Input bits:", "".join(map(str, bits)))

    pal, start = longest_palindrome(bits)
    print(f"Longest palindrome: {pal} (length {len(pal)}, starts at index {start})")

    name, encode, decode = choose_line_code()
    signal = encode(bits)
    print("Signal:", signal)
    plot_signal(signal, name)

    if input("Decode the signal? (y/n) ").strip().lower() == "y":
        decoded = decode(signal)
        print("Decoded:", "".join(map(str, decoded)))
        print("Match  :", decoded == bits)


if __name__ == "__main__":
    main()