# Utils
import numpy as np
from tqdm import tqdm
from multiprocessing import Process
import json
import matplotlib.pyplot as plt
import pickle
#Pybewego
from pybewego.numerical_optimization.ipopt_mo import NavigationOptimization
from pybewego.motion_optimization import CostFunctionParameters
from pybewego.workspace_viewer_server import WorkspaceViewerServer, WorkspaceViewerServerPlanar
from pybewego.motion_optimization import MotionOptimization
from pybewego.motion_optimization import CostFunctionParameters

#Pyrieef
from pyrieef.geometry.workspace import *
from pyrieef.motion.trajectory import *
from pyrieef.utils.collision_checking import *
from pyrieef.graph.shortest_path import *
#from trajectory import *

# Working Environment
from toy_gym.envs.toy_tasks.toy_pickplace_tamp import ToyPickPlaceTAMP
from toy_gym.policy.TAMPActionExecutor import TAMPActionExecutor

# Motion planning
from motion_planning.core.workspace import WorkspaceFromEnv
from motion_planning.core.action import *
from motion_planning.core.TAMP_motion_planner import TAMPMotionOptimizer

# Logic planning
from logic_planning.planner import LogicPlanner
from logic_planning.parser import PDDLParser
from logic_planning.action import DurativeAction
from logic_planning.helpers import frozenset_of_tuples
domain_file = "/home/nkquynh/gil_ws/tamp_logic_planner/PDDL_scenarios/domain_toy_gym.pddl"
problem_file = "/home/nkquynh/gil_ws/tamp_logic_planner/PDDL_scenarios/problem_toy_gym.pddl"
domain = PDDLParser.parse_domain(domain_file)
problem = PDDLParser.parse_problem(problem_file)

#print("Problem", problem.positive_goals)

pickled_problem = pickle.dumps(domain)
new_problem = pickle.loads(pickled_problem)
print("abcxyz", new_problem)
#problem.positive_goals = [frozenset({('at', 'object_0', 'target_1'), ('agent-free',), ('at', 'object_1', 'target_2'), ('at', 'object_2', 'target_4'), ('at', 'object_4', 'target_0'), ('at', 'object_3', 'target_3')})]
TRAJ_LENGTH = 50
DRAW_MODE = "pyglet2d" 
NB_POINTS = 40
DEBUG = False
NUM_EPS = 10
MAX_STEPS = 10000
VIEWER_ENABLE = True

planner = LogicPlanner(domain)
planner.init_planner(problem=problem, ignore_cache=False)


paths, act_seq = planner.plan(alternative=True)

action_list = []

for action in act_seq[0]:
    temp_dict = action.get_dict()
    action_list.append(temp_dict)


skeleton = []
for data in action_list:
    temp_action = DurativeAction()
    temp_action.set_from_dict(data)
    skeleton.append(temp_action)


action_list = pickle.dumps(act_seq[0])
#print("action_list", action_list)
skeleton = pickle.loads(action_list)
#print("skeleton", skeleton)

goal = problem.get_dict()["positive_goal"]
print(goal)
# for i in range(5):
#     pick = MoveToPick(parameters=["object_{}".format(i)],duration=10)
#     action_list.append(pick)
#     place = MoveToPlace(parameters=["object_{}".format(i), "target_{}".format(i)], duration=10)
#     action_list.append(place)


# goal = {"object_0": "target_1", "object_1": "target_2", "object_2": "target_0", "object_3": "target_4", "object_4": "target_3"}

with open("/home/nkquynh/gil_ws/tamp_queue_server/examples/sample_workspace.json") as f:
    data = json.load(f)
env = ToyPickPlaceTAMP(render=VIEWER_ENABLE, json_data=data, goal=goal)

costs = []
dones = []
success_episode = 0
for i in range(NUM_EPS):
    workspace_objects = env.get_workspace_objects()
    workspace = WorkspaceFromEnv(workspace_objects)
    planner = TAMPMotionOptimizer(workspace, skeleton=skeleton, enable_global_planner=False, enable_viewer=VIEWER_ENABLE, flexible_traj_ratio=4)
    planner.execute_plan()
    planner.visualize_final_trajectory()
    print("Total cost", planner.get_total_cost())
    costs.append(planner.get_total_cost())
    policy=TAMPActionExecutor(env, threshold_angle=0.5)
    policy.set_action_list(skeleton)
    for _ in range(MAX_STEPS):
        action = policy.get_action()
        obs, reward, done, info = env.step(action)
        print("logic_state", env.get_logic_state())
        if done:
            dones.append(i)
            success_episode +=1
            break
    env.reset()
    del planner
    del policy


# print("Success rate {}/{}".format(success_episode, NUM_EPS))
# print("Episode dones ", dones)
# print(costs)
# plt.plot(costs)
# plt.show()