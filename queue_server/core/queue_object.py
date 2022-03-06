

import google_auth_oauthlib
from queue_server.common_object.problem import Problem
from queue_server.common_object.domain import Domain
from pyrieef.motion.trajectory import *

class TaskQueueObject(object):
    def __init__(self, geomtric_state = None, domain: Domain = None, problem: Problem = None, trajectory = None):
        self.geometric_state = geomtric_state
        self.domain = domain
        self.problem = problem
        if self.problem is not None:
            self.logic_state = self.problem.state
            self.goal = self.problem.positive_goals
        self.trajectory = trajectory
        if self.trajectory is None:
            self.trajectory = Trajectory(T=1)

class MotionQueueObject(object):
    def __init__(self, is_refined = False, geometric_state = None, domain: Domain = None, problem: Problem = None, skeleton=None):
        self.geometric_state = geometric_state
        self.problem = problem
        self.is_refined = is_refined
        self.domain = domain
        if self.problem is not None:
            self.logic_state = self.problem.state
            self.goal = self.problem.positive_goals
        self.skeleton = skeleton