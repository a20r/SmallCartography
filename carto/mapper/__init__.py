
__all__ = ["config", "pageserver", "restful", "heart"]

import config
import pageserver
import restful
import heart


def run(host, port, ns_host, ns_port, name):
    """

    Runs the server.

    @param host The host for the server

    @param port The port for the server

    """
    hb = heart.Heart(name, host, port, ns_host, ns_port, 1)
    hb.register()
    # hb.start()
    # config.app.run(host=host, port=int(port), debug=True, use_reloader=False)
