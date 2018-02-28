import numpy as np
import math as m
from board import *

def main():
    import matplotlib
    matplotlib.use('TKAgg')
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    import sys

    if len(sys.argv) > 1:
        skip_per_frame = int(float(sys.argv[1]))
    else:
        skip_per_frame = 10

    fig = plt.figure()

    b = Board()
    im = plt.imshow(b.food.copy(), animated=True)

    def animate(i):
        for i in range(skip_per_frame):
            act      = np.zeros((NUM_ANTS, ACT_LEN))
            act[:,1] = np.random.randint(0,3,(NUM_ANTS))
            b.update(act)

        im.set_array(b.food.copy())

        return im,

    ani = animation.FuncAnimation(fig, animate, blit=False)
    plt.colorbar()
    plt.show()



if __name__ == "__main__":


    main()
