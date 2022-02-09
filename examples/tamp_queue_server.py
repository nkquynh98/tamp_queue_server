from queue_server.core.server import QueueServer


server = QueueServer()
#server.task_generator.generate_task(is_random=True)
while(1):
    server.wait_for_request()

