
import threading


class Heart(object):

    def __init__(self, name, ns_host, ns_port):
        self.host = ns_host
        self.port = ns_port

    def register(self):
        pass

    def start(self):
        pass

    def __beat(self):
        pass

    def __thread_loop(self):
        pass
