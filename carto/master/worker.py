
import time


class WorkerType(object):
    MAPPER = "mapper"
    REDUCER = "reducer"
    MASTER = "master"


class Worker(object):

    def __init__(self, name, host, port, w_type):
        self.name = name
        self.host = host
        self.port = port
        self.w_type = w_type
        self.last_update = time.time()

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def get_type(self):
        return self.w_type

    def get_name(self):
        return self.name

    def get_last_update(self):
        return self.last_update

    def update_time(self):
        self.last_update = time.time()
        return self

    def still_alive(self, mbt):
        return time.time() - self.last_time <= mbt

    def __str__(self):
        s_name = "{}:".format(self.name)
        s_host = "Host: {}".format(self.host)
        s_port = "Port: {}".format(self.port)
        s_type = "Type: {}".format(self.w_type)
        s_time = "Update time: {}".format(self.last_time)
        return "{}\n\t{}\n\t{}\n\t{}\n\t{}".format(
            s_name, s_host, s_port, s_type, s_time)

    def __repr__(self):
        return "Worker(name={}, host={}, port={}, w_type={})".format(
            self.name, self.host, self.port, self.w_type)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return other.get_host() == self.host and other.get_port() == self.port

    def __ne__(self, other):
        return not self == other


def make(*args):
    return Worker(*args)
