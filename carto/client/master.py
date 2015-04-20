
import requests


class MasterStub(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.address = "http://{}:{}".format(host, port)

    def count(self, filename):
        with open(filename) as f:
            route = self.address + "/count"
            payload = {"text": f.read()}
            r = requests.post(route, data=payload)
            return r.json()
