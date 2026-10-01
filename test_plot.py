import matplotlib.pyplot as plt

bits = [1, 0, 1, 1, 0]
levels = [1 if b == 1 else -1 for b in bits]
levels.append(levels[-1])  # so the last bit gets drawn fully

plt.step(range(len(levels)), levels, where="post")
plt.ylim(-2, 2)
plt.title("NRZ-L: 1 0 1 1 0")
plt.show()