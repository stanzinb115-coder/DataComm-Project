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

WAVEFORMS = {
    "1": ("Sine",     lambda k, n, a: a * math.sin(2 * math.pi * k / n)),
    "2": ("Square",   lambda k, n, a: a if k < n / 2 else -a),
    "3": ("Triangle", lambda k, n, a: a * (1 - 4 * abs(k / n - 0.5))),
}


def get_digital_data():
    n = int(input("How many bits? "))
    kind = input("Random data (1) or data with zero runs (2)? ").strip()

    if kind == "2":
        run_length = int(input("Run length (4 or 8)? "))
        return generate_with_zero_runs(n, run_length=run_length, num_runs=2), None
    return generate_random(n), None


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
    fig, ax = plt.subplots(figsize=(12, 3))
    line, = ax.step(range(len(levels)), levels, where="post")
    ax.set_ylim(-2, 2)
    ax.set_title(title)
    plt.show()
    return list(line.get_ydata())[:-1]   # levels read back from the plot


def plot_staircase(levels, title, where="post", analog=None):
    plt.figure(figsize=(10, 4))
    if analog is not None:
        plt.plot(analog, label="Analog signal")
    plt.step(range(len(levels)), levels, where=where, label="Staircase")
    plt.legend()
    plt.title(title)
    plt.show()


def get_samples():
    for key, (name, _) in WAVEFORMS.items():
        print(f"  {key}. {name}")
    _, wave = WAVEFORMS[input("Waveform: ").strip()]
    amplitude = float(input("Amplitude (for example 3)? "))
    n = int(input("Number of samples (for example 40)? "))
    return [wave(k, n, amplitude) for k in range(n)], amplitude


def get_dm_bits():
    samples, _ = get_samples()
    step = float(input("DM step size (for example 0.5)? "))
    bits = dm_encode(samples, step=step)

    def rebuild(b):
        return dm_decode(b, step=step)

    plot_staircase(rebuild(bits), "Delta modulation", "post", samples)
    return bits, rebuild


def get_pcm_bits():
    samples, amplitude = get_samples()
    n_bits = int(input("Bits per sample (for example 3)? "))
    bits = pcm_encode(samples, n_bits, -amplitude, amplitude)

    def rebuild(b):
        return pcm_decode(b, n_bits, -amplitude, amplitude)

    plot_staircase(rebuild(bits), "Pulse code modulation", "mid", samples)
    return bits, rebuild


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
    bits, rebuild = get_input_bits()
    print("Input bits:", "".join(map(str, bits)))

    pal, start = longest_palindrome(bits)
    print(f"Longest palindrome: {pal} (length {len(pal)}, starts at index {start})")

    name, encode, decode = choose_line_code()
    if name in ("B8ZS", "HDB3"):
        plain = ami_encode(bits)
        print("AMI signal (no scrambling):", plain)
        plot_signal(plain, "AMI (no scrambling)")

    signal = encode(bits)
    print(f"{name} signal:", signal)
    plotted = plot_signal(signal, name)

    if input("Decode the signal? (y/n) ").strip().lower() == "y":
        decoded = decode(plotted)   # decodes from the plotted levels only
        print("Decoded:", "".join(map(str, decoded)))
        print("Match  :", decoded == bits)
        if rebuild:                 # analog input: decoder staircase
            plot_staircase(rebuild(decoded), "Decoder staircase (from decoded bits)")


if __name__ == "__main__":
    main()