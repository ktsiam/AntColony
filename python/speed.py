from board import *
import numpy as np


import time

start = time.time()
b = Board()

loops = 1000

for i in range(loops):
    act      = np.zeros((NUM_ANTS, ACT_LEN), dtype=int)
    act[:,1] = np.random.randint(-1,2,(NUM_ANTS))


    b.update(act)
end = time.time()
total = end - start
print(total, "per update: ", total/ loops)
