import command
import communication
from publish_decoder import PublishDecoder
from game_state import GameState
from algorithm_fast import AlgorithmFast
from algorithm_slow import AlgorithmSlow
from algorithm_aiming import AlgorithmAiming
import threading

class Player(object):
    def __init__(self, comm, game_info, client_token):
        self.commands = command.Command()
        self.comm = comm
        self.game_info = game_info
        self.pub_decoder = PublishDecoder(game_info)
        self.game_state = GameState()
        self.comm_lock = threading.Lock()
        self.game_state_lock = threading.Lock()
        self.client_token = client_token
        self.algorithm_slow = AlgorithmSlow(self.comm, self.comm_lock, self.game_state, self.game_state_lock, self.client_token)
        self.algorithm_fast = AlgorithmFast(self.comm, self.comm_lock, self.game_state, self.game_state_lock, self.client_token)
        self.algorithm_aiming = AlgorithmAiming(self.comm, self.comm_lock, self.game_state, self.game_state_lock, self.client_token)

    def play_game(self):
        print "STARTING play_game"
        stop = False
        self.algorithm_slow.daemon = True
        self.algorithm_slow.start()
        self.algorithm_fast.daemon = True
        self.algorithm_fast.start()
        self.algorithm_aiming.daemon = True
        self.algorithm_aiming.start()

        while not stop:
            # get a message
            message = self.get_message()
            print message
            # decode it
            self.game_state_lock.acquire()
            decoded = self.pub_decoder.decode(message, self.game_state)
            self.game_state_lock.release()


    def get_message(self):
        exception_raised = False
        message = None
        while not exception_raised:
            try:
                message = self.comm.receive_pub_no_block()

                # deal with it. if it is anything except a GAMESTATE message, we will need to reset the game
                self.pub_decoder.quick_decode(message, self.game_state)

            except:
                exception_raised = True

        if message is not None:
            return message
        else:
            # there was nothing waiting for us in the queue, we will have to wait for a new message
            # the algorithm is too speedy
            return self.comm.receive(communication.Communication.Origin.PublishSocket)