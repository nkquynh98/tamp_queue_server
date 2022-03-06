import queue
import socket
import os
import json
import pickle

from queue_server.core.queue_object import TaskQueueObject, MotionQueueObject
from queue_server.core.toy_task_generator import toy_task_generator
from queue_server.common_object.parser import PDDLParser
from queue_server.common_object.message import Message
from queue import Queue

class QueueServer:
    def __init__(self, host = "127.0.0.1", port = 64563, env = "toy_gym", task_generator = toy_task_generator):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.socket.bind((host,port))
        self.configuration_folder = os.path.dirname(os.path.realpath(__file__))+"/../../configurations/"
        self.cache_folder = os.path.dirname(os.path.realpath(__file__))+"/../../cache"
        self.domain = PDDLParser.parse_domain(self.configuration_folder+"domain_"+env+".pddl")
        self.problem = PDDLParser.parse_problem(self.configuration_folder+"problem_"+env+".pddl")
        with open(self.configuration_folder+"config_"+env+".json") as f:
            self.init_config = json.load(f)

        self.task_generator = task_generator(self.domain, self.problem, self.init_config)
        self.task_queue = Queue(100)
        self.motion_queue = Queue(500)
        #print(self.init_config)

    
    def wait_for_request(self):
        self.socket.listen()
        conn, addr = self.socket.accept()
        with conn:
            recevied_data = conn.recv(100000)
            return_value = self.handle_request(recevied_data)
            #recevied_data = pickle.loads(recevied_data)
            if return_value is not None:
                conn.sendall(return_value)
        #self.socket.close()

    def handle_request(self, received_data):
        message = pickle.loads(received_data)
        if not isinstance(message, Message):
            print("InvalidMessage")
            return_message = Message(message.node_name, "Error", "InvalidMessage")
            return pickle.dumps(return_message)
        return_message = None

        if "TaskNode" in message.node_name:
            return_message = self.handle_task_node_request(message)
        elif "MotionNode" in message.node_name:
            return_message = self.handle_motion_node_request(message)
        return pickle.dumps(return_message)
    def handle_task_node_request(self, request):
        return_message = Message(request.node_name)
        if request.command == "GetDomain":
            return_message.set_command("Domain", pickle.dumps(self.domain))
        elif request.command == "GetTaskProblem":
            if self.task_queue.empty():
                self.task_queue.put(self.task_generator.generate_task(is_random = True))
            return_message.set_command("TaskProblem", pickle.dumps(self.task_queue.get()))
        elif request.command == "PutMotionProblem":
            if self.motion_queue.full():
                return_message.set_command("Error", "MotionQueueIsFull")
            else:
                motion_object = pickle.loads(request.data)
                if isinstance(motion_object, MotionQueueObject):
                    self.motion_queue.put(motion_object)
                    # for action in motion_object.skeleton:
                    #     print(action)
                    return_message.set_command("Successful", [])
                else: 
                    return_message.set_command("Error", "InvalidMessage")
        return return_message

    def handle_motion_node_request(self, request):
        return_message = Message(request.node_name)
        if request.command == "GetMotionProblem":
            if self.motion_queue.empty():
                return_message.set_command("Error", "NoMotionProblem")
            else:
                return_message.set_command("MotionProblem", pickle.dumps(self.motion_queue.get()))
        return return_message

    