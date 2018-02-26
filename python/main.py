import numpy as np
import math as m
import matplotlib.pyplot as plt


def main():
    return 1

DIM = 200
NUM_ANTS = 50

LOOK_RNG = 1
LOOK_N = LOOK_RNG ** 2

## Tile field enums
TILE_LEN = 2
T_FOOD = 0
T_TRAIL = 1

OBS_LEN = 18
O_FOOD = 0
O_Trail = 9

ACT_LEN = 2
A_LIN = 0
A_ROT = 1

offsetTable = np.array([(a,b) for a in range(-1,2) for b in range(-1,2)])

class Board(object):
    def __init__(self, dim=DIM, num_ants=NUM_ANTS):
        self.dim = dim
        self.num_ants = num_ants

        self.board = np.random.normal(50, 2, (dim,dim,TILE_LEN) )



        self.obs   = np.zeros((num_ants, OBS_LEN),dtype=float)

        self.Ants  = {i:Ant(_ID=i) for i in range(NUM_ANTS)}


    def update(self, action):
        """
        Args: action: np.ndarray((NUM_ANTS, ACT_LEN), dtype=float)
        """
        self.board += np.random.normal(10,8,(DIM,DIM,TILE_LEN))

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

            (x,y) = (int(ant.x), int(ant.y))

            for k in range(LOOK_RNG):
                for j in range(LOOK_RNG):
                    (f,t) = self.board[x+k-1][y+j-1]
                    self.obs[i][k*LOOK_RNG + j]            = f
                    self.obs[i][(k*LOOK_RNG + j + LOOK_N)] = t
            z[x][y] = int(ant.theta * 10)
            # z[x][y] = "HI"

            # neighbors = np.array([int(ant.x), int(ant.y)]) + offsetTable
        plt.figure(figsize=(9,9))
        plt.imshow(self.board[:,:,0]);
        plt.colorbar()
        plt.show()

class Ant(object):
    def __init__(self, x_pos=DIM/2, y_pos=DIM/2, _theta=0, _ID=0):
        self.x = x_pos
        self.y = y_pos
        self.theta = _theta # 0 to 2pi

        self.dx = 0
        self.dy = 0

        self.food = 100.0

        self.ID = _ID
