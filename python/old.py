import numpy as np
import math as m

import matplotlib.pyplot as plt


def main():
    import matplotlib
    matplotlib.use('TKAgg')
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation

    fig = plt.figure()

    b = Board()
    def scale_b(board):
        bo = board[:,:,0]
        bo *= 10 / np.mean(bo)
        return bo
    im = plt.imshow(scale_b(b.board), animated=True)

    def animate(i):
        act1 = np.random.normal(2, 0.8,(NUM_ANTS))
        act2 = np.random.normal(0.2, 1,(NUM_ANTS))
        act = np.dstack((act1, act2)).reshape(NUM_ANTS,2)
        act[:,1] *= 2
        act[:,1] -= np.mean(act[:,1])/2
        b.update(act)
        im.set_array(scale_b(b.board))

        return im,

    ani = animation.FuncAnimation(fig, animate, np.arange(1,DIM**2), interval=25, blit=False)
    plt.colorbar()
    plt.show()


DIM = 500
NUM_ANTS = 5000

LOOK_RNG = 1
LOOK_N = LOOK_RNG ** 2

## Tile field enums
TILE_LEN = 1
T_FOOD = 0
# T_TRAIL = 1

OBS_LEN = 9
O_FOOD = 0
# O_Trail = 9

ACT_LEN = 2
A_LIN = 0
A_ROT = 1

offsetTable = np.array([(a,b) for a in range(-1,2) for b in range(-1,2)])

class Board(object):
    def __init__(self, dim=DIM, num_ants=NUM_ANTS):
        self.dim = dim
        self.num_ants = num_ants




        self.targets = np.zeros((DIM,DIM,2),dtype=float)
        for x in range(DIM):
            for y in range(DIM):
                self.targets[x][y][0] = Board.calc_targets(x,y)
        self.board = self.targets.copy()



        self.obs   = np.zeros((num_ants, OBS_LEN),dtype=float)

        self.Ants  = {i:Ant(_ID=i) for i in range(NUM_ANTS)}

    @staticmethod
    def calc_targets( x,y):
        x_1, y_1 = (DIM/3, DIM/2)
        return 100*(1.0001)**(-(x-x_1)**2-(y-y_1)**2)


    def update(self, action):
        """
        Args: action: np.ndarray((NUM_ANTS, ACT_LEN), dtype=float)
        """
        # self.board += np.random.normal(10,8,(DIM,DIM,TILE_LEN))


        # self.board += (self.targets ** 2) / (15 * self.board + 1)
        self.board += 0.10*self.targets*(1 - (self.board)/(self.targets+0.0001))



        z = np.zeros((DIM,DIM), dtype=int)
        for (i,ant) in enumerate(self.Ants.values()):
            ant.theta = (ant.theta + action[i][A_ROT]) % (2* m.pi)

            ant.x += action[i][A_LIN] * m.cos(ant.theta)
            ant.y += action[i][A_LIN] * m.sin(ant.theta)

            (x,y) = (int(ant.x), int(ant.y))

            tile = self.board[x][y]

            ant.food += (tile[T_FOOD] / 2)
            tile[T_FOOD] /= 2
            if tile[T_FOOD] > 20.0:
                tile[T_FOOD] -= 5.0
                ant.food -= 100.0
            else:
                ant.food -= 95.0

            # (x,y) = (int(ant.x), int(ant.y))

            for k in range(LOOK_RNG):
                for j in range(LOOK_RNG):
                    f = self.board[x+k-1][y+j-1][0]

                    # (f,t) = self.board[x+k-1][y+j-1]
                    self.obs[i][k*LOOK_RNG + j]            = f

                    # self.obs[i][(k*LOOK_RNG + j + LOOK_N)] = t
            z[x][y] = int(ant.theta * 10)
            # z[x][y] = "HI"

            # neighbors = np.array([int(ant.x), int(ant.y)]) + offsetTable

class Ant(object):
    def __init__(self, x_pos=DIM/2, y_pos=DIM/2, _theta=0, _ID=0):
        self.x = x_pos
        self.y = y_pos
        self.theta = _theta # 0 to 2pi

        self.dx = 0
        self.dy = 0

        self.food = 100.0

        self.ID = _ID

if __name__ == "__main__":
    main()
