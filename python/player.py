import command
import communication
from publish_decoder import PublishDecoder
from game_state import GameState
from algorithm import Algorithm


class Player(object):
    def __init__(self, comm, game_info):
        self.commands = command.Command()
        self.comm = comm
        self.game_info = game_info
        self.pub_decoder = PublishDecoder(game_info)
        self.game_state = GameState()
        self.algorithm = Algorithm(self.game_state, self.comm)

    def play_game(self, client_token):
        # TODO: later, we will want to spawn two threads here
        stop = False
        while not stop:
            # get a message
            message = self.get_message()

            # decode it
            decoded = self.pub_decoder.decode(message, self.game_state)

            # decide what to do
            if decoded == "GAMESTATE":
                try:
                    self.algorithm.make_move(client_token)
                except Exception as e:
                    if len(e.args) == 1 and e.args[0] == 'too many iterations':
                        continue
                    else:
                        raise
                #stop = True

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
