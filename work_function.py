import time
import random
import math

N = 10000

start = time.perf_counter()

with open("./data.txt", "w") as f:
  f.write("\n")

for i in range(N):

  if random.random() > 0.9:
    with open("./data.txt", "a") as f:
      content = f.write(f"{(time.perf_counter() - start)}\t{100 * i / N}\n")

  valore = (2) ** (i * 0.011) * 0.0001
  # time.sleep(random.random() * valore)
  time.sleep(0.01)


with open("./data.txt", "a") as f:
  content = f.write(f"{(time.perf_counter() - start)}\t{100}\n")