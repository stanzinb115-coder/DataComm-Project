import matplotlib.pyplot as plt
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


def main():
    bits = get_digital_data()
    print("Digital data:", "".join(map(str, bits)))

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