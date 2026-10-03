import random # loads Python's built-in random number module


def generate_random(n):
    """Completely random bit sequence of length n."""

    return [random.randint(0, 1) for _ in range(n)] #picks either 0 or 1, each with equal chance. Both ends are included. and brackets for list comprehension 

#_ is just a variable name, (THROWAWAY VARIABLE), used because the loop index isn't needed.

# Complexity: O(n), because it makes exactly n random picks.


def generate_with_zero_runs(n, run_length=8, num_runs=2):
    # n is the total length, run_length is how many zeros in each run (8 or 4), and num_runs is how many runs to plant. The =8 and =2 are default values, used if you don't pass anything.

    """Random bits with `num_runs` fixed runs of `run_length` consecutive zeros planted in."""
    bits = generate_random(n)  #starts with a fully random list
    for _ in range(num_runs):
        start = random.randint(0, n - run_length) #picks a random position where the run will begin
        bits[start:start + run_length] = [0] * run_length

 # [0] * run_length makes a list of zeros. [0] * 4 gives [0, 0, 0, 0].
#. bits[start:start + run_length] = ... is slice assignment. It replaces that section of the list with the new values.
#Example: bits = [1,1,0,1,1,1,0,1], start = 2, run_length = 4:
#the slice bits[2:6] is [0,1,1,1]
#it gets replaced by [0,0,0,0]
#result: [1,1,0,0,0,0,0,1]

    return bits

print(generate_with_zero_runs(20, run_length=4, num_runs=2))
#Complexity is O(n) for generating the random list, plus O(run_length × num_runs) for planting. Overall O(n).

def longest_palindrome(bits):
    """Longest palindromic substring using Manacher's algorithm, O(n).
    Returns (palindrome_string, start_index)."""
    s = "".join(map(str, bits)) #map(str, bits) converts each number to a string: [1,0,1] → "1", "0", "1".
    if not s:
        return "", 0

    t = "#" + "#".join(s) + "#"      # separators make odd/even palindromes uniform
    n = len(t)
    p = [0] * n                      # p[i] = palindrome radius centred at i
    center = right = 0

    for i in range(n):
        if i < right:
            p[i] = min(right - i, p[2 * center - i])   # reuse the mirror's result
        while i + p[i] + 1 < n and i - p[i] - 1 >= 0 and t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1
        if i + p[i] > right:
            center, right = i, i + p[i]

    max_len, center_idx = max((v, i) for i, v in enumerate(p))
    start = (center_idx - max_len) // 2
    return s[start:start + max_len], start





# SIMPLE VERSION 
def expand(s, left, right):
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1 # starting from both left and right from the middle , then checking values at that index if it matches then 
                   #start expanding outwards like left-1 & right +1 and again check the values and go onn till the while loop fails 
        right += 1 
    return left + 1, right - 1


def longest_palindrome_simple(bits):
    s = "".join(map(str, bits))
    if not s:
        return "", 0

    best_start, best_end = 0, 0

    for i in range(len(s)):
        l1, r1 = expand(s, i, i)        # odd-length palindrome centred on i
        l2, r2 = expand(s, i, i + 1)    # even-length palindrome centred between i and i+1

        if r1 - l1 > best_end - best_start:
            best_start, best_end = l1, r1
        if r2 - l2 > best_end - best_start:
            best_start, best_end = l2, r2

    return s[best_start:best_end + 1], best_start




if __name__ == "__main__":
    bits = generate_with_zero_runs(30, run_length=4, num_runs=2)
    print("Bits:", "".join(map(str, bits)))
    pal, start = longest_palindrome(bits)
    print(f"Longest palindrome: {pal} (length {len(pal)}, starts at index {start})")
    print("Simple:  ", longest_palindrome_simple(bits))

# for simple version 
    s = "1011"
start, end = expand(s, 1, 1)
print(start, end, s[start:end + 1])