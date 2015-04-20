
import threading
import requests
import time


class Heart(object):

    def __init__(self, name, host, port, ns_host, ns_port, wait_time):
        self.name = name
        self.host = host
        self.port = port
        self.ns_host = ns_host
        self.ns_port = ns_port
        self.wait_time = wait_time
        self.address = "http://{}:{}".format(ns_host, ns_port)
        self.thread = None
        self.running = False

    def register(self):
        route = self.address + "/register"
        payload = {
            "name": self.name,
            "host": self.host,
            "port": self.port,
            "type": "reducer"
        }

        r = requests.post(route, data=payload)
        return r

    def start(self):
        self.running = True
        thr = threading.Thread(target=self.__thread_loop)
        thr.daemon = True
        thr.start()

    def stop(self):
        self.running = False

    def __beat(self):
        route = self.address + "/beat"
        payload = {"name": self.name}
        r = requests.post(route, data=payload)
        return r

    def __thread_loop(self):
        while self.running:
            self.__beat()
            time.sleep(self.wait_time)
