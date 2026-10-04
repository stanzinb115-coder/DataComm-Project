import matplotlib.pyplot as plt
from encoders import nrz_l_encode, nrz_l_decode
from encoders import nrz_i_encode, nrz_i_decode
from encoders import manchester_encode, manchester_decode

# To add a new line code later: import it above and add one line here
SCHEMES = {
    "NRZ-L": (nrz_l_encode, nrz_l_decode),
    "NRZ-I": (nrz_i_encode, nrz_i_decode),
    "Manchester": (manchester_encode, manchester_decode),
}

while True:
    print()
    print("Schemes:", ", ".join(SCHEMES))
    name = input("Which scheme? (or type q to quit) ").strip()
    if name.lower() == "q":
        break
    if name not in SCHEMES:
        print("Unknown scheme, try again")
        continue

    text = input("Enter bits (like 10110): ").strip()
    bits = [int(c) for c in text]

    encode, decode = SCHEMES[name]
    signal = encode(bits)

    print("Signal :", signal)
    print("Decoded:", decode(signal))
    print("Match  :", decode(signal) == bits)

    levels = signal + [signal[-1]]
    plt.figure(figsize=(12, 3))
    plt.step(range(len(levels)), levels, where="post")
    plt.ylim(-2, 2)
    plt.title(name + ": " + text)
    plt.show()