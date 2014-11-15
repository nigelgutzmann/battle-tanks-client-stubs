from game_state import GameState
from publish_decoder import PublishDecoder
from gameinfo import GameInfo
import json

gs = GameState()
gi = GameInfo('ThinkTank2.0', '', '')
pd = PublishDecoder(gi)
message = """{"timeRemaining": 101.94638109207153, "map": {"terrain": [{"boundingBox": {"corner": [30, 30], "size": [15, 15]}, "type": "SOLID"}, {"boundingBox": {"corner": [70, 30], "size": [15, 15]}, "type": "SOLID"}, {"boundingBox": {"corner": [110, 30], "size": [15, 15]}, "type": "SOLID"}, {"boundingBox": {"corner": [150, 30], "size": [15, 15]}, "type": "SOLID"}, {"boundingBox": {"corner": [30, 70], "size": [15, 15]}, "type": "SOLID"}, {"boundingBox": {"corner": [70, 70], "size": [15, 15]}, "type": "SOLID"}, {"boundingBox": {"corner": [110, 70], "size": [15, 15]}, "type": "SOLID"}, {"boundingBox": {"corner": [150, 70], "size": [15, 15]}, "type": "SOLID"}, {"boundingBox": {"corner": [30, 30], "size": [15, 15]}, "type": "SOLID"}, {"boundingBox": {"corner": [70, 30], "size": [15, 15]}, "type": "SOLID"}, {"boundingBox": {"corner": [110, 30], "size": [15, 15]}, "type": "SOLID"}, {"boundingBox": {"corner": [150, 30], "size": [15, 15]}, "type": "SOLID"}, {"boundingBox": {"corner": [30, 70], "size": [15, 15]}, "type": "SOLID"}, {"boundingBox": {"corner": [70, 70], "size": [15, 15]}, "type": "SOLID"}, {"boundingBox": {"corner": [110, 70], "size": [15, 15]}, "type": "SOLID"}, {"boundingBox": {"corner": [150, 70], "size": [15, 15]}, "type": "SOLID"}], "size": [200, 112.5]}, "match_id": "5eca0d40-f296-4036-afb7-70eef351afaf", "players": [{"score": 1, "name": "ThinkTank2.0", "tanks": [{"alive": true, "projectiles": [], "tracks": 1.4148306223055802, "hitRadius": 2.0, "speed": 10.0, "id": "5c068916-3552-4e62-8c7a-9c57996cc55b", "turret": 0.6584702545442362, "health": 100.0, "collisionRadius": 2.0, "position": [189.06, 70.53000000000002], "type": "TankFast"}, {"alive": true, "projectiles": [{"position": [22.640000000000214, 59.41999999999982], "direction": 3.1715416412080506, "speed": 30.0, "id": "2c95dead-004c-41f5-bd43-3948d868080e", "damage": 100.0}], "tracks": 4.912419068809372, "hitRadius": 2.0, "speed": 5.0, "id": "3a84e610-c983-4574-a596-c16583b770fa", "turret": 3.1715416412080506, "health": 200.0, "collisionRadius": 2.0, "position": [181.24000000000024, 66.14999999999998], "type": "TankSlow"}]}, {"score": 3, "name": "testclient", "tanks": [{"alive": true, "projectiles": [{"position": [177.42711781158914, 70.10613962243382], "direction": 0.036730490268009924, "speed": 30.0, "id": "b970bd32-24ba-40d0-a637-3a4e0e537c57", "damage": 100.0}], "tracks": 0.06396224548544134, "hitRadius": 2.0, "speed": 10.0, "id": "1f96311d-6d7f-40c4-b4e7-886de5d449eb", "turret": 0.06396224548544134, "health": 100.0, "collisionRadius": 2.0, "position": [151.76876978622116, 68.0], "type": "TankFast"}, {"alive": true, "projectiles": [{"position": [192.4, 54.540000000000006], "direction": 2.1107919161008497, "speed": 30.0, "id": "d1feb7ca-4cf4-428e-8f22-96f9ad2b34a8", "damage": 100.0}], "tracks": 5.072027940852145, "hitRadius": 2.0, "speed": 5.0, "id": "50233744-eb19-4fd5-b979-4035495bf754", "turret": 2.2753770341366333, "health": 200.0, "collisionRadius": 2.0, "position": [195.17, 50.35], "type": "TankSlow"}]}], "timestamp": 1416015401906.47, "comm_type": "GAMESTATE"}"""
pd.decode(message, gs)
ef = json.loads(message)['players'][1]['tanks'][0]['position']
es = json.loads(message)['players'][1]['tanks'][1]['position']
route = gs.get_route_for_slow(es)

if len(route) > 3:
    next_point = route[2]
elif len(route) > 2:
    next_point = route[1]

ignore, position = gs.get_closest_enemy_to_slow()
gs.get_target_point_for_tank_at_for_slow(position)