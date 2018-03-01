import numpy as np
import math as m

DIM = 100
INV_DIM = 1 / DIM
NUM_ANTS = 1

LOOK_RNG = 1
LOOK_N = LOOK_RNG ** 2

## Tile field enums
TILE_LEN = 1
T_FOOD = 0
# T_TRAIL = 1

OBS_LEN = 3 # l,f,r food
O_FOOD = 0
# O_Trail = 9

ACT_LEN = 2
A_LIN = 0
A_ROT = 1

SPLIT_FOOD = 600


class Board(object):
    def __init__(self, dim=DIM, num_ants=NUM_ANTS):
        self.dim = dim
        self.num_ants = num_ants
        self.rot_arr = np.array([-m.pi/3, 0, m.pi/3])

        self.gen_coord = (DIM/4, DIM/(3))

        self.targets = np.zeros((DIM,DIM),dtype=float)
        for x in range(DIM):
            for y in range(DIM):
                self.targets[x][y] = self.calc_targets(x,y,90)

        self.gen_coord = (3*DIM/4, 2*DIM/(3))
        for x in range(DIM):
            for y in range(DIM):
                self.targets[x][y] += self.calc_targets(x,y,60)

        self.gen_coord = (DIM - (DIM/9), DIM/(9))
        for x in range(DIM):
            for y in range(DIM):
                self.targets[x][y] += self.calc_targets(x,y,70, 3.5)

        start = np.random.normal(0.7, 0.01,(DIM,DIM))
        self.food = self.targets.copy() * start


        self.obs   = np.zeros((num_ants, OBS_LEN),dtype=float)
        self.id_ant_count = NUM_ANTS
        self.Ants  = [Ant(_ID=i) for i in range(NUM_ANTS)]


    def calc_targets(self, x,y, strength=100, tightness=1.0):
        """
        Calculates upper bounds for food per tile using a 2D normal dist

        for larger spread make exp_const smaller (ie less food near edges)
        """

        x_1, y_1 = self.gen_coord
        exp_const = INV_DIM * 0.035 * tightness
        exp = exp_const * (-(x-x_1) ** 2 - (y-y_1) ** 2)
        noise = np.random.normal(1, 0.05)
        if noise < 0.3:
            noise = 0.3

        return strength  *  (2 ** exp) * noise


    def growth_food(self, rate=0.10):
        self.food[self.food < 0] = 1

        reg = (1 - (self.food)/(self.targets+0.0001))
        reg = self.targets * reg
        noise = np.random.normal(1,0.2)

        return rate * noise * reg

    def get_obs(self, index, ant):
        """ obs - shape (NUM_ANTS, OBS_LEN)"""
        obs = self.obs[index]
        new_thetas = (ant.theta + self.rot_arr) % (2*m.pi)

        new_coords = [ (ant.x + 1.5*m.cos(ang), ant.y + 1.5*m.sin(ang)) for ang in new_thetas]
        obs = np.array([self.food[int(x)][int(y)] for (x,y) in new_coords])
        self.obs[index] = obs


    def board_bounds(self, ant):
        # ant.x = ((1 + ant.x) % (DIM - 3) - 1)
        # ant.y = ((1 + ant.y) % (DIM - 3) - 1)
        if ant.x > (DIM - 2):
            ant.x -= 10
        elif ant.x < (2):
            ant.x += 10
        if ant.y > (DIM - 2):
            ant.y -= 10
        elif ant.y < (2):
            ant.y += 10

    def update(self, action):
        """
        Args: action: np.ndarray((NUM_ANTS, ACT_LEN), dtype=float)
        actually ints
        """
        self.food += self.growth_food(0.0005) # 0.005


        for (i,ant) in enumerate(self.Ants):
            dTheta = (action[i][A_ROT] - 1) * m.pi/3  ## action is 0, 1, 2 (l,f,r)
            ant.theta = (ant.theta + dTheta) % (2 * m.pi)
            dist = 1

            ant.x += dist * m.cos(ant.theta)
            ant.y += dist * m.sin(ant.theta)

            self.board_bounds(ant)

            (x,y) = (int(ant.x), int(ant.y))

            tile_f = self.food[x][y]

            ant.food += (tile_f / 2)
            tile_f /= 2
            if tile_f > 20.0:
                tile_f -= 5.0
                ant.food -= 10.0
            else:
                ant.food -= 5.0
            self.food[x][y] = tile_f

            # kill ant if it has no food


        ant_list = []
        ## split / kill
        for (i,ant) in enumerate(self.Ants):
            if ant.food > 0:
                ant_list.append(ant)
                if ant.food > SPLIT_FOOD:
                    new_ant = Ant(ant.x, ant.y, np.random.uniform(0, m.pi * 2),
                              _food = ant.food / 2)
                    ant_list.append(new_ant)
                    ant.food /= 2.0
        self.Ants = ant_list
        NUM_ANTS = len(self.Ants)

        self.obs   = np.zeros((NUM_ANTS, OBS_LEN),dtype=float)
        # get obs for each ants
        # ensure ants within board
        for (i,ant) in enumerate(self.Ants):
            self.board_bounds(ant)
            self.get_obs(i, ant)


        return self.obs.copy()


        @staticmethod
        def check_angle(ang):
            """ Ensures angle is between 0 and 2PI """
            return ang % (2 * m.pi)

class Ant(object):
    def __init__(self, x_pos=DIM/2, y_pos=DIM/2, _theta=0, _ID=0, _food=50):
        self.x = x_pos + np.random.normal(0, DIM/20)
        self.y = y_pos + np.random.normal(0, DIM/20)
        self.theta = _theta # 0 to 2pi



        self.dx = 0
        self.dy = 0

        self.food = _food

        self.ID = _ID
