
__all__ = ["pageserver", "robots", "coordinators"]


import pageserver
import robots
import coordinators
import config


def run(host, port):
    """

    Runs the server.

    @param host The host for the server

    @param port The port for the server

    """
    config.app.run(host=host, port=int(port), debug=True, use_reloader=False)
