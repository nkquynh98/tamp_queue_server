import json
from types import SimpleNamespace
from motion_planning.core.workspace import WorkspaceFromEnv
from toy_gym.envs.toy_tasks.toy_pickplace_fiveobject import ToyPickPlaceFiveObject
import socket
VIEWER_ENABLE = False
HOST, PORT = "localhost", 9999
env = ToyPickPlaceFiveObject(render=VIEWER_ENABLE, map_name="maze_world", is_object_random=True, is_target_random=True)
#print(env.workspace_objects.get_dict())
data = env.workspace_objects.get_dict()
with open('/home/nkquynh/gil_ws/queue_server/sample.json', 'w') as f:
    json.dump(data, f)
data = json.dumps(data)


print("data", data)
x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
print(x._map)
