import socket
import os
import json
import pickle
import random

from queue_server.core.queue_object import TaskQueueObject, MotionQueueObject
from queue_server.common_object.domain import Domain
from queue_server.common_object.problem import Problem
from queue_server.common_object.message import Message
from queue_server.common_object.helpers import frozenset_of_tuples
def bound(low, high, value):
    return max(low, min(high, value))

class toy_task_generator:
    def __init__(self, domain: Domain, init_problem: Problem, init_configuration):
        self.domain = domain
        self.target = domain.constants["location"]
        self.object = domain.constants["object"]        
        self.problem = init_problem
        self.configuaration = init_configuration

    def generate_task(self, is_random=False):
        if is_random:
            map_dim = self.configuaration["_map"]["_map_dim"]
            object_target = random.sample(self.target, k = len(self.object))
            object_target_dict = {}
            for i, object in enumerate(self.object):                
                random_pos = [round(bound(-4,4,(random.random()-0.5)*dim),3) for dim in map_dim]
                self.configuaration["_movable_obstacles"][object]["_position"] = random_pos
                object_target_dict[object] = object_target[i]
            #print(self.problem.positive_goals)
            new_goal = []
            for pred in self.problem.positive_goals[0]:
                if pred[0] == "at":
                    new_pred = ["at", pred[1], object_target_dict[pred[1]]]
                else:
                    new_pred = list(pred)
                new_goal.append(new_pred)
            new_goal_set = frozenset_of_tuples(new_goal)
            self.problem.positive_goals[0] = new_goal_set
            #print(self.problem.positive_goals)
        task_object = TaskQueueObject(self.configuaration, self.domain, self.problem)    
        return task_object