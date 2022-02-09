#!/usr/bin/env python3
# Logic planning
from logic_planning.planner import LogicPlanner
from logic_planning.parser import PDDLParser
from logic_planning.action import DurativeAction
from logic_planning.helpers import frozenset_of_tuples
domain_file = "/home/nkquynh/gil_ws/tamp_logic_planner/PDDL_scenarios/domain_toy_gym.pddl"
problem_file = "/home/nkquynh/gil_ws/tamp_logic_planner/PDDL_scenarios/problem_toy_gym.pddl"
domain = PDDLParser.parse_domain(domain_file)
problem = PDDLParser.parse_problem(problem_file)

import socket
import json
import pickle
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65433     # Port to listen on (non-privileged ports are > 1023)
with open("/home/nkquynh/gil_ws/tamp_queue_server/sample_workspace.json") as f:
    data = json.load(f)
data = json.dumps(data)
send_data = bytes(data,encoding="utf-8")
print(domain.get_dict())

pickled_problem = pickle.dumps(domain)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        #conn.send(send_data)
        conn.send(pickled_problem)
        #a = conn.recv(1024)
        print(a)
        
