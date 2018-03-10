from time import time
import numpy as np

SIZE = 100000 # ten thousand

a1 = np.random.random((SIZE)).tolist()
a2 = np.random.random((SIZE)).tolist()

t1 = time()

sums = 0
for i in range(10000):
    sums += a1[i] + a2[i]

t2 = time()
print(sums,"time: ", t2 -t1)
