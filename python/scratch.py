from game_state import GameState
from publish_decoder import PublishDecoder
from gameinfo import GameInfo
import json

gs = GameState()
gi = GameInfo('ThinkTank2.0', '', '')
pd = PublishDecoder(gi)
message = {u'timeRemaining': -0.013342142105102539, u'map': {u'terrain': [{u'boundingBox': {u'corner': [18, 60], u'size': [5, 35]}, u'type': u'SOLID'}, {u'boundingBox': {u'corner': [23, 90], u'size': [10, 5]}, u'type': u'SOLID'}, {u'boundingBox': {u'corner': [23, 75], u'size': [10, 5]}, u'type': u'SOLID'}, {u'boundingBox': {u'corner': [33, 80], u'size': [5, 10]}, u'type': u'SOLID'}, {u'boundingBox': {u'corner': [23, 80], u'size': [10, 10]}, u'type': u'IMPASSABLE'}, {u'boundingBox': {u'corner': [59, 75], u'size': [5, 10]}, u'type': u'IMPASSABLE'}, {u'boundingBox': {u'corner': [54, 65], u'size': [5, 15]}, u'type': u'IMPASSABLE'}, {u'boundingBox': {u'corner': [64, 65], u'size': [5, 15]}, u'type': u'IMPASSABLE'}, {u'boundingBox': {u'corner': [54, 60], u'size': [15, 5]}, u'type': u'IMPASSABLE'}, {u'boundingBox': {u'corner': [49, 50], u'size': [5, 15]}, u'type': u'IMPASSABLE'}, {u'boundingBox': {u'corner': [69, 50], u'size': [5, 15]}, u'type': u'IMPASSABLE'}, {u'boundingBox': {u'corner': [59, 65], u'size': [5, 10]}, u'type': u'SOLID'}, {u'boundingBox': {u'corner': [93, 70], u'size': [10, 5]}, u'type': u'SOLID'}, {u'boundingBox': {u'corner': [88, 60], u'size': [5, 10]}, u'type': u'SOLID'}, {u'boundingBox': {u'corner': [103, 65], u'size': [5, 5]}, u'type': u'SOLID'}, {u'boundingBox': {u'corner': [93, 55], u'size': [10, 5]}, u'type': u'SOLID'}, {u'boundingBox': {u'corner': [103, 45], u'size': [5, 10]}, u'type': u'SOLID'}, {u'boundingBox': {u'corner': [93, 40], u'size': [10, 5]}, u'type': u'SOLID'}, {u'boundingBox': {u'corner': [88, 45], u'size': [5, 5]}, u'type': u'SOLID'}, {u'boundingBox': {u'corner': [126, 60], u'size': [10, 5]}, u'type': u'IMPASSABLE'}, {u'boundingBox': {u'corner': [126, 30], u'size': [10, 5]}, u'type': u'IMPASSABLE'}, {u'boundingBox': {u'corner': [121, 35], u'size': [20, 5]}, u'type': u'IMPASSABLE'}, {u'boundingBox': {u'corner': [121, 55], u'size': [20, 5]}, u'type': u'IMPASSABLE'}, {u'boundingBox': {u'corner': [121, 40], u'size': [5, 15]}, u'type': u'IMPASSABLE'}, {u'boundingBox': {u'corner': [136, 40], u'size': [5, 15]}, u'type': u'IMPASSABLE'}, {u'boundingBox': {u'corner': [126, 40], u'size': [10, 15]}, u'type': u'SOLID'}, {u'boundingBox': {u'corner': [155, 20], u'size': [5, 35]}, u'type': u'SOLID'}, {u'boundingBox': {u'corner': [160, 40], u'size': [5, 10]}, u'type': u'SOLID'}, {u'boundingBox': {u'corner': [165, 30], u'size': [5, 15]}, u'type': u'SOLID'}, {u'boundingBox': {u'corner': [170, 25], u'size': [5, 10]}, u'type': u'SOLID'}, {u'boundingBox': {u'corner': [175, 20], u'size': [5, 35]}, u'type': u'SOLID'}], u'size': [200, 112.5]}, u'match_id': u'b62e8267-9cef-4ff3-8c95-8edb4423d20f', u'timestamp': 1416007418191.067, u'players': [{u'score': 9, u'name': u'testclient', u'tanks': [{u'turret': 6.074162364373322, u'type': u'TankFast', u'alive': True, u'projectiles': [], u'tracks': 2.324032360659568, u'health': 100.0, u'collisionRadius': 2.0, u'hitRadius': 2.0, u'position': [95.0, 68.0], u'speed': 10.0, u'id': u'06dc16ce-0147-4fee-bb0f-75c5310933dc'}, {u'turret': 3.4078447027407184, u'type': u'TankSlow', u'alive': True, u'projectiles': [], u'tracks': 3.7079075975618854, u'health': 200.0, u'collisionRadius': 2.0, u'hitRadius': 2.0, u'position': [105.0, 57.0], u'speed': 5.0, u'id': u'd552c785-003f-4155-b864-ce6bcdbfe3d8'}]}, {u'score': 1, u'name': u'ThinkTank2.0', u'tanks': [{u'turret': 3.184541528237682, u'type': u'TankFast', u'alive': True, u'projectiles': [], u'tracks': 3.8053438710584415, u'health': 100.0, u'collisionRadius': 2.0, u'hitRadius': 2.0, u'position': [194, 47], u'speed': 10.0, u'id': u'd117eb5e-1fcc-42d1-bc40-656b5c8656a4'}, {u'turret': 6.1918548086725975, u'type': u'TankSlow', u'alive': True, u'projectiles': [], u'tracks': 5.838902068923362, u'health': 200.0, u'collisionRadius': 2.0, u'hitRadius': 2.0, u'position': [83, 51], u'speed': 5.0, u'id': u'f10c5fe5-ec3b-431e-b38f-5a9b19f05cdf'}]}], u'comm_type': u'GAMESTATE'}
pd.decode(json.dumps(message), gs)

# enemy tanks are at: [95.0, 68.0] and [105.0, 57.0]
ef = [95.0, 68.0]
es = [105.0, 57.0]
route = gs.get_route_for_fast(ef)