import command
import communication
from publish_decoder import PublishDecoder
from game_state import GameState
from algorithm import Algorithm
import threading

class Player(object):
    def __init__(self, comm, game_info):
        self.commands = command.Command()
        self.comm = comm
        self.game_info = game_info
        self.pub_decoder = PublishDecoder(game_info)
        self.game_state = GameState()
        self.comm_lock = threading.Lock()
        self.game_state_lock = threading.Lock()
        self.algorithm = Algorithm(self.comm, self.comm_lock, self.game_state, self.game_state_lock)

    def play_game(self, client_token):
        print "STARTING play_game"
        stop = False
        self.algorithm.deamon = True
        self.algorithm.run(client_token)
        while not stop:
            # get a message
            message = self.get_message()

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
