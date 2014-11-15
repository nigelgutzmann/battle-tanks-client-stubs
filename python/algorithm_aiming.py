from command import Command
import math
from path_finding import Point
import threading
import copy


class AlgorithmAiming(threading.Thread):
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
        print "STARTING run() - AlgorithmAiming"

        commands = Command(self.client_token)
        stop = False
        while not stop:
            if self.game_state is None:
                print "GAME STATE IS NONE!!!!"
                continue

            self.copy_real_game_state()
            if self.game_state.fast_exists() and not self.game_state.enemies_exist():
                stop_command = commands.getStopCommand(
                    self.game_state.get_fast_tank_id(),
                    'FIRE',
                )
                self.send_command(stop_command)

            if self.game_state.slow_exists() and not self.game_state.enemies_exist():
                stop_command = commands.getStopCommand(
                    self.game_state.get_slow_tank_id(),
                    "FIRE",
                )
                self.send_command(stop_command)

            if self.game_state.fast_exists():
                distance_to_target, position_of_target = self.game_state.get_closest_enemy_to_fast()

                # get the turret rotation
                #target_point = self.game_state.get_target_point_for_tank_at_for_fast(position_of_target)
                target_point = Point(position_of_target[0], position_of_target[1])
                turret_angle = self.__get_target_angle(self.game_state.get_position_for_fast(), target_point)
                change_turret_angle = turret_angle - self.game_state.get_fast_tank_turret_angle()

                turret_rotate_command = commands.getTurretRotateCommand(
                    self.game_state.get_fast_tank_id(),
                    change_turret_angle
                )

                self.send_command(turret_rotate_command)

                # send the fire command
                if self.game_state.enemies_exist() and change_turret_angle < math.pi / 6:
                    tank_fire_command = commands.getFireCommand(self.game_state.get_fast_tank_id())
                else:
                    # stop the fire command!!!
                    tank_fire_command = commands.getStopCommand(
                        self.game_state.get_fast_tank_id(),
                        'FIRE',
                    )
                self.send_command(tank_fire_command)

            if self.game_state.slow_exists():
                distance_to_target, position_of_target = self.game_state.get_closest_enemy_to_slow()

                # get the turret rotation
                #target_point = self.game_state.get_target_point_for_tank_at_for_slow(position_of_target)
                target_point = Point(position_of_target[0], position_of_target[1])
                turret_angle = self.__get_target_angle(self.game_state.get_position_for_slow(), target_point)
                change_turret_angle = turret_angle - self.game_state.get_slow_tank_turret_angle()

                turret_rotate_command = commands.getTurretRotateCommand(
                    self.game_state.get_slow_tank_id(),
                    change_turret_angle
                )

                self.send_command(turret_rotate_command)

                # send the fire command
                if self.game_state.enemies_exist() and change_turret_angle < math.pi / 6:
                    tank_fire_command = commands.getFireCommand(self.game_state.get_slow_tank_id())
                else:
                    tank_fire_command = commands.getStopCommand(
                        self.game_state.get_slow_tank_id(),
                        "FIRE"
                    )
                self.send_command(tank_fire_command)

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
        self.game_state = copy.deepcopy(self.real_game_state)
        self.game_state_lock.release()
