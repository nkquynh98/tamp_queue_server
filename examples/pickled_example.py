# Utils
import numpy as np
from tqdm import tqdm
from multiprocessing import Process
import json
import matplotlib.pyplot as plt
import pickle



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

print("abcxyz", new_problem.get_dict())