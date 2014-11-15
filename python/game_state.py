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
    def __init__(self, _map=[], enemy_slow=None, enemy_fast=None, me_slow=None, me_fast=None, enemy_slow_old_position=None, enemy_fast_old_position=None):
        self.__map = _map
        self.__enemy_slow = enemy_slow
        self.__enemy_fast = enemy_fast
        self.__me_slow = me_slow
        self.__me_fast = me_fast
        self.__enemy_slow_old_position = enemy_slow_old_position
        self.__enemy_fast_old_position = enemy_fast_old_position

    # FUNCTIONS TO SET UP THE MAP
    def copy_gs(self):
        new_map = []
        for row in self.__map:
            new_map.append(row[:])
        new_enemy_slow = self.__enemy_slow.copy()
        new_enemy_fast = self.__enemy_fast.copy()
        new_me_slow = self.__me_slow.copy()
        new_me_fast = self.__me_fast.copy()
        new_enemy_slow_old_position = self.__enemy_slow_old_position[:]
        new_enemy_fast_old_position = self.__enemy_fast_old_position[:]

        return GameState(
            _map=new_map,
            enemy_slow=new_enemy_slow,
            enemy_fast=new_enemy_fast,
            me_slow=new_me_slow,
            me_fast=new_me_fast,
            enemy_slow_old_position=new_enemy_slow_old_position,
            enemy_fast_old_position=new_enemy_fast_old_position
        )

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
            elif ter['type'] == 'IMPASSABLE':
                spot = 1
            else:
                # we initialized everything to zero already
                return

            x_start = int(round(ter['boundingBox']['corner'][0], 0))
            y_start = int(round(ter['boundingBox']['corner'][1], 0))
            x_len = int(round(ter['boundingBox']['size'][0], 0))
            y_len = int(round(ter['boundingBox']['size'][1], 0))

            for x in range(x_len):
                for y in range(y_len):
                    if (x_start + x) < len(self.__map) and (y_start + y) < len(self.__map[0]):
                        # sometimes the terrain is too big to fit onto the map
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
        self.__me_slow = None
        self.__me_fast = None
        self.__enemy_fast = None
        self.__enemy_slow = None

    def set_enemy_position(self, slow_tank=None, fast_tank=None):
        self.__enemy_fast = fast_tank
        self.__enemy_slow = slow_tank

    def set_my_position(self, slow_tank=None, fast_tank=None):
        self.__me_fast = fast_tank
        self.__me_slow = slow_tank

    # FUNCTIONS USED BY THE ALGORITHM
    def slow_exists(self):
        return self.__me_slow is not None and self.__me_slow['alive']

    def fast_exists(self):
        return self.__me_fast is not None and self.__me_fast['alive']

    def enemies_exist(self):
        return self.__enemy_slow is not None or self.__enemy_fast is not None

    def get_all_projectiles(self):
        tanks = self.__get_all_tanks()
        projectiles = []
        for tank in tanks:
            projectiles.extend(tank['projectiles'])
        return projectiles

    def get_track_rotation_for_slow(self):
        if self.__me_slow is not None:
            return self.__me_slow['tracks']
        else:
            return 0

    def get_track_rotation_for_fast(self):
        if self.__me_fast is not None:
            return self.__me_fast['tracks']
        else:
            return 0

    def get_closest_enemy_to_slow(self):
        return self.__get_closest_enemy_to(self.__me_slow)

    def get_closest_enemy_to_fast(self):
        return self.__get_closest_enemy_to(self.__me_fast)

    def get_furthest_enemy_to_slow(self):
        return self.__get_furthest_enemy_to(self.__me_slow)

    def get_furthest_enemy_to_fast(self):
        return self.__get_furthest_enemy_to(self.__me_fast)

    def get_route_for_slow(self, target):
        return self.__get_route_to(self.__me_slow, target)

    def get_route_for_fast(self, target):
        return self.__get_route_to(self.__me_fast, target)

    def get_position_for_fast_exact(self):
        if self.__me_fast is not None:
            return self.__me_fast['position']
        else:
            return self.__get_center()

    def get_position_for_slow_exact(self):
        if self.__me_slow is not None:
            return self.__me_slow['position']
        else:
            return self.__get_center()

    def get_position_for_slow(self):
        if self.__me_slow is not None:
            return Point(self.__me_slow['position'][0], self.__me_slow['position'][1])
        else:
            center = self.__get_center()
            return Point(center[0], center[1])

    def get_position_for_fast(self):
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

    def get_slow_tank_turret_angle(self):
        if self.__me_slow is not None:
            return self.__me_slow['turret']
        else:
            return 0

    def get_fast_tank_turret_angle(self):
        if self.__me_fast is not None:
            return self.__me_fast['turret']
        else:
            return 0

    def get_target_point_for_tank_at_for_fast(self, position):
        tank = None
        position_point = Point(position[0], position[1])
        if self.__enemy_fast is not None and self.__enemy_fast['position'] == position:
            if self.__enemy_fast_old_position and \
                abs(self.__enemy_fast['position'][0] - self.__enemy_fast_old_position[0]) < 0.1 and \
                abs(self.__enemy_fast['position'][1] - self.__enemy_fast_old_position[1]) < 0.1:
                # he's probably not moving, just return the same thing
                return position_point
            # the other function (for the slow tank sets __enemy_fast_old_position and __enemy_slow_old_position)
            # so we don't need to here
            tank = self.__enemy_fast
        elif self.__enemy_slow is not None and self.__enemy_slow['position'] == position:
            if self.__enemy_slow_old_position and \
                abs(self.__enemy_slow['position'][0] - self.__enemy_slow_old_position[0]) < 0.1 and \
                abs(self.__enemy_slow['position'][1] - self.__enemy_slow_old_position[1]) < 0.1:
                # he's probably not moving, just return the same thing
                return position_point
            # the other function (for the slow tank sets __enemy_fast_old_position and __enemy_slow_old_position)
            # so we don't need to here
            tank = self.__enemy_slow

        if tank is None:
            # there wasn't a matching tank, return the same thing
            return position_point

        return self.__get_target_point_for_tank_at(tank, self.__me_fast)

    def get_target_point_for_tank_at_for_slow(self, position):
        tank = None
        position_point = Point(position[0], position[1])
        if self.__enemy_fast is not None and self.__enemy_fast['position'] == position:
            if self.__enemy_fast_old_position and \
                abs(self.__enemy_fast['position'][0] - self.__enemy_fast_old_position[0]) < 0.1 and \
                abs(self.__enemy_fast['position'][1] - self.__enemy_fast_old_position[1]) < 0.1:
                # he's probably not moving, just return the same thing
                return position_point

            # assume he's moving, set the old position for the next iteration
            self.__enemy_fast_old_position = position
            tank = self.__enemy_fast
        elif self.__enemy_slow is not None and self.__enemy_slow['position'] == position:
            if self.__enemy_slow_old_position and \
                abs(self.__enemy_slow['position'][0] - self.__enemy_slow_old_position[0]) < 0.1 and \
                abs(self.__enemy_slow['position'][1] - self.__enemy_slow_old_position[1]) < 0.1:
                # he's probably not moving, just return the same thing
                return position_point

            # assume he's moving, set the old position for the next iteration
            self.__enemy_slow_old_position = position
            tank = self.__enemy_slow

        if tank is None:
            # there wasn't a matching tank, return the same thing
            return position_point

        return self.__get_target_point_for_tank_at(tank, self.__me_slow)


    def __get_target_point_for_tank_at(self, enemy, my_tank):
        enemy_position = Point(enemy['position'][0], enemy['position'][1])
        my_position = Point(my_tank['position'][0], my_tank['position'][1])

        # assume projectiles travel at 30m/s
        # just use the distance between my_tank and enemy as a proxy for the distance
        # to the final intersection
        distance_from_target = enemy_position.distance_to(my_position)

        # v = d / t --> t = d / v
        time_to_intersect = distance_from_target / 30.0

        # v = d / t --> d = t * v
        distance_tank_can_travel = time_to_intersect * enemy['speed']

        distance_tank_can_travel_x = distance_tank_can_travel * math.cos(enemy['tracks'])
        distance_tank_can_travel_y = distance_tank_can_travel * math.sin(enemy['tracks'])

        # tanks don't usually go in straight lines. try dividing by something to reduce the effect
        distance_tank_can_travel_x = 0.75 * distance_tank_can_travel_x
        distance_tank_can_travel_y = 0.75 * distance_tank_can_travel_y
        return Point(
            enemy_position.x + distance_tank_can_travel_x,
            enemy_position.y + distance_tank_can_travel_y
        )
        


    def __get_all_tanks(self):
        tank_list = [self.__me_slow, self.__me_fast, self.__enemy_slow, self.__enemy_fast]
        return [tank for tank in tank_list if tank is not None]

    def __get_enemies(self):
        enemies = [self.__enemy_fast, self.__enemy_slow]
        return [tank for tank in enemies if tank is not None and tank['alive']]

    def __get_route_to(self, tank, target):
        # returns a list of Points of the path that we should take
        if tank is not None:
            path_finder = PathFinder(self.__map, target, tank['position'], self.get_all_projectiles(), None)
            return path_finder.get_path()
        else:
            center = self.__get_center()
            center_p = Point(center[0], center[1])
            return [center_p, center_p]

    def __get_furthest_enemy_to(self, tank):
        if tank is None:
            return (9999, self.__get_center())
        elif self.__enemy_slow is None and self.__enemy_fast is None:
            return (9999, self.__get_center())
        elif self.__enemy_slow is None:
            return (self.__get_direct_distance(tank, self.__enemy_fast), self.__enemy_fast['position'])
        elif self.__enemy_fast is None:
            return (self.__get_direct_distance(tank, self.__enemy_slow), self.__enemy_slow['position'])
        else:
            slow_dist = self.__get_direct_distance(tank, self.__enemy_slow)
            fast_dist = self.__get_direct_distance(tank, self.__enemy_fast)
            if slow_dist < fast_dist:
                return (fast_dist, self.__enemy_fast['position'])
            else:
                return (slow_dist, self.__enemy_slow['position'])

    def __tank_exists(self, tank):
        return tank is not None and tank['alive']

    def __get_closest_enemy_to(self, tank):
        if tank is None:
            # force the tank to go to the center
            return (9999, self.__get_center())
        elif not self.__tank_exists(self.__enemy_slow) and not self.__tank_exists(self.__enemy_fast):
            # force the tank to go to the center
            return (9999, self.__get_center())
        elif not self.__tank_exists(self.__enemy_slow):
            return (self.__get_direct_distance(tank, self.__enemy_fast), self.__enemy_fast['position'])
        elif not self.__tank_exists(self.__enemy_fast):
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
