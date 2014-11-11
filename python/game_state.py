import math
from path_finding import PathFinder, Point


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

    # FUNCTIONS TO SET UP THE MAP
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
        y_iter = range(y_len)
        y_iter.reverse()
        for y in y_iter:
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

    # FUNCTIONS USED BY THE ALGORITHM
    def get_turret_rotation_for_slow(self):
        if self.__me_slow is not None:
            return self.__me_slow['tracks']
        else:
            return 0

    def get_turret_rotation_for_fast(self):
        if self.__me_fast is not None:
            return self.__me_fast['tracks']
        else:
            return 0

    def get_closest_enemy_to_slow(self):
        return self.__get_closest_enemy_to(self.__me_slow)

    def get_closest_enemy_to_fast(self):
        return self.__get_closest_enemy_to(self.__me_fast)

    def get_route_for_slow(self, target):
        return self.__get_route_to(self.__me_slow, target)

    def get_route_for_fast(self, target):
        return self.__get_route_to(self.__me_fast, target)

    def get_position_for_slow(self):
        if self.__me_slow is not None:
            return Point(self.__me_slow['position'][0], self.__me_slow['position'][1])
        else:
            center = self.__get_center()
            return Point(center[0], center[1])

    def get_posotion_for_fast(self):
        if self.__me_fast is not None:
            return Point(self.__me_fast['position'][0], self.__me_fast['position'][1])
        else:
            center = self.__get_center()
            return Point(center[0], center[1])

    def get_slow_tank_id(self):
        if self.__me_slow is not None:
            return self.__me_slow['id']
        else:
            return ""

    def get_fast_tank_id(self):
        if self.__me_fast is not None:
            return self.__me_fast['id']
        else:
            return ""

    def __get_route_to(self, tank, target):
        # returns a list of Points of the path that we should take
        if tank is not None:
            path_finder = PathFinder(self.__map, target, tank['position'])
            return path_finder.get_path()
        else:
            center = self.__get_center()
            center_p = Point(center[0], center[1])
            return [center_p, center_p]

    def __get_closest_enemy_to(self, tank):
        if tank is None:
            # force the tank to go to the center
            return (9999, self.__get_center())
        elif self.__enemy_slow is None and self.__enemy_fast is None:
            # force the tank to go to the center
            return (9999, self.__get_center())
        elif self.__enemy_slow is None:
            return (self.__get_direct_distance(tank, self.__enemy_fast), self.__enemy_fast['position'])
        elif self.__enemy_fast is None:
            return (self.__get_direct_distance(tank, self.__enemy_slow), self.__enemy_slow['position'])
        else:
            slow_dist = self.__get_direct_distance(tank, self.__enemy_slow)
            fast_dist = self.__get_direct_distance(tank, self.__enemy_fast)
            if slow_dist < fast_dist:
                return (slow_dist, self.__enemy_slow['position'])
            else:
                return (fast_dist, self.__enemy_fast['position'])

    def __get_direct_distance(self, tank_1, tank_2):
        tank_1_x = tank_1['position'][0]
        tank_1_y = tank_1['position'][1]
        tank_2_x = tank_2['position'][0]
        tank_2_y = tank_2['position'][1]
        return self.__get_point_distance(tank_1_x, tank_1_y, tank_2_x, tank_2_y)

    def __get_point_distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y1)**2)

    def __get_center(self):
        if self.__map is None or len(self.__map) == 0:
            return [0, 0]
        else:
            return [len(self.__map) / 2, len(self.__map[0]) / 2]
