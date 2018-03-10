from kostas_board import *
# from board import *
import time


s = time.time()
b = Board()

obs = np.random.random((NUM_ANTS, OBS_LEN))

act      = np.zeros((NUM_ANTS, ACT_LEN), dtype=int)
act[:,1] = obs.argmax(axis=1)
obs = b.update(act)

for i in range(100):
    act      = np.zeros((len(b.ants), ACT_LEN), dtype=int)
    act[:,1] = obs.argmax(axis=1)
    obs = b.update(act)
f = time.time()
print(f - s)
