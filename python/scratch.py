from game_state import GameState
from publish_decoder import PublishDecoder
from gameinfo import GameInfo
import json

gs = GameState()
gi = GameInfo('ThinkTank2.0', '', '')
pd = PublishDecoder(gi)
message = """{"timeRemaining": 3.159122943878174, "map": {"terrain": [{"boundingBox": {"corner": [0, 45], "size": [200, 30]}, "type": "IMPASSABLE"}], "size": [200, 112.5]}, "match_id": "29d71080-2a6e-4c5e-a9df-3ef10666da46", "players": [{"score": 21, "name": "testclient", "tanks": [{"alive": true, "projectiles": [{"position": [74.90999999999964, 77.57999999999996], "direction": 0.45866553473846033, "speed": 30.0, "id": "e409fa16-6396-4aaf-a0b4-2beba06cb393", "damage": 100.0}, {"position": [18.459999999999674, 51.19], "direction": 0.4456147380540907, "speed": 30.0, "id": "1525b4bb-e57b-4c80-84f8-58d70ca9e59c", "damage": 100.0}], "tracks": 1.924890541697061, "hitRadius": 2.0, "speed": 5.0, "id": "7e20767d-494f-415e-b80d-cb12a2d0b735", "turret": 0.4451059060972414, "health": 200.0, "collisionRadius": 2.0, "position": [2.0299999999996716, 43.0], "type": "TankSlow"}]}, {"score": 0, "name": "ThinkTank2.0", "tanks": [{"alive": true, "projectiles": [], "tracks": 0.5104476209834452, "hitRadius": 2.0, "speed": 10.0, "id": "96df5b50-4941-4981-9cb5-d50e4c384266", "turret": 1.500758594427206, "health": 100.0, "collisionRadius": 2.0, "position": [167, 78], "type": "TankFast"}, {"alive": true, "projectiles": [], "tracks": 5.899862439060031, "hitRadius": 2.0, "speed": 5.0, "id": "c3f5676b-4270-4df9-9846-d3359620abcf", "turret": 0.1843227157403668, "health": 100.0, "collisionRadius": 2.0, "position": [132, 105], "type": "TankSlow"}]}], "timestamp": 1416017402531.696, "comm_type": "GAMESTATE"}"""
pd.decode(message, gs)
ef = json.loads(message)['players'][1]['tanks'][0]['position']
es = json.loads(message)['players'][1]['tanks'][1]['position']
mf = json.loads(message)['players'][0]['tanks'][0]['position']
ms = json.loads(message)['players'][0]['tanks'][1]['position']
route = gs.get_route_for_fast(es)

if len(route) > 3:
    next_point = route[2]
elif len(route) > 2:
    next_point = route[1]

ignore, position = gs.get_closest_enemy_to_slow()
gs.get_target_point_for_tank_at_for_slow(position)
