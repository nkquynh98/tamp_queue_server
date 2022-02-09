class Message:
    def __init__(self, node_name:str, command=None, data=None):
        self.node_name = node_name
        self.command = command
        self.data = data

    def set_command(self, command: str, data):
        self.command = command
        self.data = data