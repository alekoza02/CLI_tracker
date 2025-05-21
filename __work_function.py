#!/usr/bin/python3

import time
import random
import math
import numpy as np


N = 1000

start = time.perf_counter()

with open("./data.txt", "w") as f:
  f.write("\n")


def mode1():
  for i in range(N):

    with open("./data.txt", "a") as f:
      content = f.write(f"{(time.perf_counter() - start)}\t{100 * i / N}\n")

    valore = (2) ** (i * 0.011) * 0.0002
    time.sleep(random.random() * valore)


def mode2():
  for i in range(N):

    if random.random() > 0.0:
      with open("./data.txt", "a") as f:
        content = f.write(f"{(time.perf_counter() - start)}\t{100 * i / N}\n")

    time.sleep(0.1)


def mode3():
  
  values = [random.random() * 1 for i in range(10)]
  values.extend([random.random() * 0.1 for i in range(50)])
  values.extend([random.random() * 1 for i in range(10)])
  values.extend([random.random() * 0.01 for i in range(10)])
  values.extend([random.random() * 2 for i in range(3)])
  values.extend([random.random() * 0.01 for i in range(17)])
  values.extend([random.random() * 0.1 for i in range(50)])
  values.extend([random.random() * 0.01 for i in range(10)])
  values.extend([random.random() * 0.1 for i in range(50)])
  values.extend([random.random() * 1 for i in range(10)])
  values.extend([random.random() * 0.01 for i in range(10)])
  values.extend([random.random() * 2 for i in range(3)])
  values.extend([random.random() * 0.01 for i in range(17)])
  values.extend([random.random() * 0.1 for i in range(50)])
  values.extend([random.random() * 2 for i in range(3)])
  values.extend([random.random() * 0.01 for i in range(17)])
  values.extend([random.random() * 0.1 for i in range(50)])
  values.extend([random.random() * 0.01 for i in range(10)])
  values.extend([random.random() * 0.1 for i in range(50)])
  values.extend([random.random() * 1 for i in range(10)])
  values.extend([random.random() * 0.01 for i in range(10)])
  values.extend([random.random() * 2 for i in range(3)])
  values.extend([random.random() * 0.01 for i in range(17)])
  values.extend([random.random() * 0.1 for i in range(50)])
  values.extend([random.random() * 0.01 for i in range(10)])

  for index, v in enumerate(values):
    with open("./data.txt", "a") as f:
      content = f.write(f"{(time.perf_counter() - start)}\t{100 * index / len(values)}\n")

    time.sleep(v)


def mode4():

  values = []
  values.extend([0.01 for i in range(100)])
  values.extend([0.1 for i in range(30)])
  values.extend([0.003 for i in range(200)])
  
  for index, v in enumerate(values):
    with open("./data.txt", "a") as f:
      content = f.write(f"{(time.perf_counter() - start)}\t{100 * index / len(values)}\n")

    time.sleep(v)


def mode5():

  def generate_file_sizes(n=3000, seed=42):
      np.random.seed(seed)
      # Generate base noise (small files)
      small_files = np.random.exponential(scale=2, size=int(n * 0.7))
      # Generate medium files with more variability
      medium_files = np.random.normal(loc=10, scale=5, size=int(n * 0.2))
      medium_files = np.clip(medium_files, 0.1, None)
      # Generate a few very large files
      large_files = np.random.lognormal(mean=4, sigma=1, size=int(n * 0.1))
      # Combine and shuffle
      all_files = np.concatenate([small_files, medium_files, large_files])
      np.random.shuffle(all_files)
      return all_files.tolist()

  file_sizes = generate_file_sizes()  

  print(np.max(file_sizes), np.min(file_sizes))

  for index, v in enumerate(file_sizes):
    with open("./data.txt", "a") as f:
      content = f.write(f"{(time.perf_counter() - start)}\t{100 * index / len(file_sizes)}\n")

    time.sleep(v / 500)



mode5()

with open("./data.txt", "a") as f:
  content = f.write(f"{(time.perf_counter() - start)}\t{100}\n")