

class GameState(object):
    '''
    The GameState is an object to represent the gameboard.

    It contains an array (__map) that holds all the points on the board.

    Points on the board can be referenced by __map[x][y]

    If a point is a 0, it is passible ground
    If a point is a 1, it is impassible ground (tanks cannot drive here)
    If a point is a 2, it is solid (tanks and bullets cannot go through here)
    '''
    def __init__(self):
        self.__map = []
        self.__enemy_slow = None
        self.__enemy_fast = None
        self.__me_slow = None
        self.__me_fast = None

    def boundaries_unset(self):
        return len(self.__map) == 0

    def set_boundaries(self, x, y):
        self.__map = []
        for i in range(x):
            self.__map.append([])
            for j in range(y):
                self.__map[i].append(0)

    def set_terrain(self, terrain=[]):
        for ter in terrain:
            spot = 0
            if ter['type'] == 'SOLID':
                spot = 2
            elif ter['type'] == 'IMPASSIBLE':
                spot = 1
            else:
                # we initialized everything to zero already
                return

            x_start = int(ter['boundingBox']['corner'][0])
            y_start = int(ter['boundingBox']['corner'][1])
            x_len = int(ter['boundingBox']['size'][0])
            y_len = int(ter['boundingBox']['size'][1])
            for x in range(x_len):
                for y in range(y_len):
                    self.__map[x_start + x][y_start + y] = spot

    def print_map(self):
        x_len = len(self.__map)
        if x_len == 0:
            print "map uninitialized"
            return

        y_len = len(self.__map[0])

        print
        for y in range(y_len):
            print
            for x in range(x_len):
                print str(self.__map[x][y]) + " ",

        print
        print

    def reset(self):
        self.__map = []

    def set_enemy_position(self, slow_tank=None, fast_tank=None):
        self.__enemy_fast = fast_tank
        self.__enemy_slow = slow_tank

    def set_my_position(self, slow_tank=None, fast_tank=None):
        self.__me_fast = fast_tank
        self.__me_slow = slow_tank
