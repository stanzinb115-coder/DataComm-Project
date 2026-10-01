import random

def generate_random(n):
    return [random.randint(0, 1) for _ in range(n)]

bits = generate_random(20)
print(bits)