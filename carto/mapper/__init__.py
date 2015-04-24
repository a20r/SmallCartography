
__all__ = ["config", "pageserver", "restful", "heart"]

import config
import pageserver
import restful
import heart
import random


def run(host, port, ns_host, ns_port, name):
    """

    Runs the server.

    @param host The host for the server

    @param port The port for the server

    """
    # random.seed(hash(name))
    hb = heart.Heart(name, host, port, ns_host, ns_port, 1)
    while True:
        try:
            hb.register()
            break
        except:
            "Trying to register..."
    hb.start()
    config.app.run(host=host, port=int(port), debug=True, use_reloader=False)
