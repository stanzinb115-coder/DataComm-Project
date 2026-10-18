from generator import generate_random, generate_with_zero_runs, longest_palindrome


def get_digital_data():
    n = int(input("How many bits? "))
    kind = input("Random data (1) or data with zero runs (2)? ").strip()

    if kind == "2":
        run_length = int(input("Run length (4 or 8)? "))
        return generate_with_zero_runs(n, run_length=run_length, num_runs=2)
    return generate_random(n)


def main():
    bits = get_digital_data()
    print("Digital data:", "".join(map(str, bits)))

    pal, start = longest_palindrome(bits)
    print(f"Longest palindrome: {pal} (length {len(pal)}, starts at index {start})")


if __name__ == "__main__":
    main()