from command import Command
import math
from path_finding import Point
import threading
import copy


class AlgorithmSlow(threading.Thread):
    def __init__(self, comm, comm_lock, real_game_state, game_state_lock, client_token):
        threading.Thread.__init__(self)
        self.comm = comm
        self.comm_lock = comm_lock
        self.real_game_state = real_game_state
        self.game_state = None
        self.game_state_lock = game_state_lock
        self.copy_real_game_state()
        self.client_token = client_token

    def run(self):
        '''
        here's what really matters...
        '''
        print "STARTING run()"

        commands = Command(self.client_token)
        stop = False
        while not stop:
            if self.game_state is None:
                print "GAME STATE IS NONE!!!!"
                continue

            self.copy_real_game_state()

            # work on the slow tank
            # find the closest enemy
            if self.game_state.slow_exists():
                distance_to_target, position_of_target = self.game_state.get_closest_enemy_to_slow()

                route = self.game_state.get_route_for_slow(position_of_target)

                # route has a list of Points that we should go through to get to the target
                # now figure out the rotation
                my_rotation = self.game_state.get_track_rotation_for_slow()
                #print "My rotation: " + str(my_rotation)

                # the first point is the point that we are currently at, so we have to take the second one in the list
                next_point = None
                if len(route) > 200:
                    next_point = route[100]
                if len(route) > 4:
                    next_point = route[3]
                if len(route) > 3:
                    next_point = route[2]
                elif len(route) > 2:
                    next_point = route[1]

                if next_point:  # if we can find a next point...
                    my_point = self.game_state.get_position_for_slow()

                    target_angle = self.__get_target_angle(my_point, next_point)

                    tank_rotate_command = commands.getTankRotateCommand(
                        self.game_state.get_slow_tank_id(),
                        target_angle - my_rotation
                    )
                    self.send_command(tank_rotate_command)

                else:
                    pass
                    """tank_forward_command = commands.getMoveCommand(
                            self.game_state.get_slow_tank_id(),
                            10,
                            direction="FWD"
                        )
                        #print "SENDING: " + str(tank_forward_command)
                        self.send_command(tank_forward_command)"""

    def __get_target_angle(self, my_point, target):

        delta_x = target.x - my_point.x
        delta_y = target.y - my_point.y

        target_angle = math.atan2(delta_y, delta_x)

        if target_angle < 0:
            target_angle = target_angle + 2 * math.pi
        if target_angle > 2 * math.pi:
            target_angle = target_angle - 2 * math.pi
        return target_angle

    def send_command(self, command):
        self.comm_lock.acquire()
        self.comm.send(command)
        self.comm_lock.release()

    def copy_real_game_state(self):
        self.game_state_lock.acquire()
        self.game_state = self.real_game_state.copy_gs()
        self.game_state_lock.release()
