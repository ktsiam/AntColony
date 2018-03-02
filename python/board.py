import numpy as np
import math as m


DIM      = 100
NUM_ANTS = 10
OBS_LEN  = 3
ACT_LEN  = 2

class Coord(object): #Coord object
    def __init__(self, _x = 0, _y = 0):
        self.x = _x
        self.y = _y

    def __add__(self, c):
        return Coord(self.x + c.x, self.y + c.y)

        
class Tile(object): #Tile object
    GROWTH_RATE     = 0.1
    INIT_FOOD_RATIO = 0.5
    PEAK_NUM        = 3
    PEAK_STRENGTH   = [60, 70, 90]
    PEAK_TIGHTNESS  = [1.0, 3.5, 1.0]
    PEAK_COORD      = [Coord(3*DIM/4, 2*DIM/3), Coord(8*DIM/9, DIM/9),
                      Coord(  DIM/4,   DIM/3)]
    
    def __init__(self, x, y):
        
        self.food_cap = 0
        for i in range(self.PEAK_NUM):
            self.food_cap += self.set_cap(Coord(x, y),
                             Tile.PEAK_COORD[i], Tile.PEAK_STRENGTH[i],
                             Tile.PEAK_TIGHTNESS[i])
        self.food = self.food_cap * Tile.INIT_FOOD_RATIO

    def grow(self):
        reg   = (1 - self.food / max (self.food_cap, 0.000001))
        noise = np.random.normal(1, 0.2)
        self.food += Tile.GROWTH_RATE * noise * reg

    def get_eaten(self):
        self.food /= 2
        if  self.food > 20.0:
            self.food -= 5
        
        
    @staticmethod
    def set_cap(p, _p, strength, tightness):
        exp_const = 0.035 * tightness / DIM
        exp   = exp_const * (-(p.x - _p.x) ** 2 - (p.y - _p.y) ** 2)
        noise = np.random.normal(1, 0.05)
        
        return noise if noise > 0.3 else 0.3

    

class Ant(object): # Ant object
    SPLIT_FOOD = 600
    A_ROT      = 1 # no idea what this is btw
    ROT_ARR    = [-m.pi/3, 0, m.pi/3]
    def __init__(self, _pos = Coord(DIM/2, DIM/2), _theta=0, _food=50):

        self.theta = _theta # [0, 2π]
        self.food  = _food
        self.pos   = _pos + Coord(np.random.normal(0, DIM/20),
                                  np.random.normal(0, DIM/20))
        self.coord = Coord(int(self.pos.x), int(self.pos.y))

    def act(self, action, tiles): 
        # action : 0, 1, 2 (left, front, right)
        dTheta       = (action[Ant.A_ROT] - 1)      *  m.pi / 3
        self.theta   = (dTheta +    self.theta) % (m.pi * 2)
        self.pos.x  += m.cos(self.theta) %  DIM
        self.pos.y  += m.sin(self.theta) %  DIM
        self.coord.x =   int(self.pos.x)
        self.coord.y =   int(self.pos.y)

        # food : ant, square
        self.eat(tiles[self.coord.x][self.coord.y].food)
        tiles         [self.coord.x][self.coord.y].get_eaten()

    def eat(self, amount):
        half = amount / 2
        self.food += (half - 10) if half > 20.0 else (half - 5)

    def is_alive(self):
        return self.food > 0

    def is_reproducible(self):
        return self.food > Ant.SPLIT_FOOD

    def observe(self, tiles):
        new_thetas = (self.theta + ROT_ARR) % (2*m.pi)
        new_xs     = int(self.pos.x + 1.5 * m.cos(new_thetas))
        new_ys     = int(self.pos.y + 1.5 * m.sin(new_thetas))
        obs        = [tiles[x][y] for (x, y) in zip(new_xs, new_ys)]
        return obs
    
class Board(object):
    def __init__(self, gen_cord = Coord(DIM/4, DIM/3)):
        self.tiles = np.zeros((DIM, DIM), dtype=Tile)
        self.ants  = []
        
        for x in range(DIM):
            for y in range(DIM):
                self.tiles[x][y] = Tile(x, y)

        for i in range(len(self.ants)):
            self.ants[i] = Ant()
        
    def update(self, actions):
        """
        Args: action: np.array((len(ants), ACT_LEN), dtype=float)
        actually ints
        """
        for x in range(DIM):
            for y in range(DIM):
                self.tiles[x][y].grow()

        for i in range(len(self.ants)):
            self.ants[i].act(actions[i], self.tiles)

        # kill and make ants

        new_ants = []
        for ant in self.ants:
            if not ant.is_alive:
                self.ants.remove(ant)
            elif ant.is_reproducible():
                ant.food /= 2
                new_ants.append(ant)
                ant.theta = random.uniform(0, 2*m.pi)

        self.ants += new_ants

        observations = np.zeros((len(self.ants), OBS_LEN), dtype=float)
        for ant in self.ants:
            observations.append(ant.observe(self.tiles))
            
        return observations
