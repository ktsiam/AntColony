import numpy as np
import math as m
from board import *

def main():
    # import matplotlib
    # matplotlib.use('TKAgg')
    # import matplotlib.pyplot as plt
    # import matplotlib.animation as animation
    import sys

    if len(sys.argv) > 1:
        skip_per_frame = int(float(sys.argv[1]))
    else:
        skip_per_frame = 10

    fig = plt.figure()

    b = Board()
    im = plt.imshow(b.food.copy(), vmin=0, vmax=110, animated=True)


    def animate(i):
        for i in range(skip_per_frame):
            # obs = np.random.random((NUM_ANTS, OBS_LEN))
            act      = np.zeros((len(b.Ants), ACT_LEN), dtype=int)
            act[:,1] = b.obs.argmax(axis=1)
            b.update(act)


        im.set_array(b.food.copy())

        return im,

    ani = animation.FuncAnimation(fig, animate, blit=False)
    plt.colorbar()
    plt.show()



if __name__ == "__main__":


    obs = np.random.random((NUM_ANTS, OBS_LEN))
    main()
