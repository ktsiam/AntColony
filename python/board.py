import numpy as np
import math as m

DIM = 400
INV_DIM = 1 / DIM
NUM_ANTS = 200

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

class Board(object):
    def __init__(self, dim=DIM, num_ants=NUM_ANTS):
        self.dim = dim
        self.num_ants = num_ants
        self.rot_arr = np.array([-m.pi/3, 0, m.pi/3])

        self.gen_coord = (DIM/4, DIM/(2.1))

        self.targets = np.zeros((DIM,DIM),dtype=float)
        for x in range(DIM):
            for y in range(DIM):
                self.targets[x][y] = self.calc_targets(x,y)

        start = np.random.normal(0.5, 0.2,(DIM,DIM))
        self.food = self.targets.copy() * start


        self.obs   = np.zeros((num_ants, OBS_LEN),dtype=float)

        self.Ants  = {i:Ant(_ID=i) for i in range(NUM_ANTS)}


    def calc_targets(self, x,y):
        """
        Calculates upper bounds for food per tile using a 2D normal dist

        for larger spread make exp_const smaller (ie less food near edges)
        """

        x_1, y_1 = self.gen_coord
        exp_const = INV_DIM * 0.015
        exp = exp_const * (-(x-x_1) ** 2 - (y-y_1) ** 2)
        noise = np.random.normal(1, 0.05)
        if noise < 0.3:
            noise = 0.3

        return 100  *  (2 ** exp) * noise


    def growth_food(self, rate=0.10):
        self.food[self.food < 0] = 1

        reg = (1 - (self.food)/(self.targets+0.0001))
        reg = self.targets * reg
        noise = np.random.normal(1,0.2)

        return rate * noise * reg

    def get_obs(self, index):
        """ obs - shape (NUM_ANTS, OBS_LEN)"""
        obs = self.obs[i]


    def update(self, action):
        """
        Args: action: np.ndarray((NUM_ANTS, ACT_LEN), dtype=float)
        actually ints
        """
        self.food += self.growth_food(0.005)

        for (i,ant) in enumerate(self.Ants.values()):

            dTheta = self.rot_arr[ action[i][A_ROT] ]  ## action is 0, 1, 2 (l,f,r)
            ant.theta = (ant.theta + dTheta) % (2 * m.pi)
            dist = .5

        ## FLOATING PNT Movement System
            # ant.theta = (ant.theta + action[i][A_ROT]) % (2* m.pi)
            ant.x += dist * m.cos(ant.theta)
            ant.y += dist * m.sin(ant.theta)


            (x,y) = (int(ant.x), int(ant.y))

            tile_f = self.food[x][y]

            ant.food += (tile_f / 2)
            tile_f /= 2
            if tile_f > 20.0:
                tile_f -= 5.0
                ant.food -= 100.0
            else:
                ant.food -= 95.0
            self.food[x][y] = tile_f



        @staticmethod
        def check_angle(ang):
            """ Ensures angle is between 0 and 2PI """
            return ang % (2 * m.pi)

class Ant(object):
    def __init__(self, x_pos=DIM/2, y_pos=DIM/2, _theta=0, _ID=0):
        self.x = x_pos + np.random.normal(0, DIM/20)
        self.y = y_pos + np.random.normal(0, DIM/20)
        self.theta = _theta # 0 to 2pi


        self.dx = 0
        self.dy = 0

        self.food = 100.0

        self.ID = _ID
