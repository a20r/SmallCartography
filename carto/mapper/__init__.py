
__all__ = ["config", "pageserver", "restful"]

import config
import pageserver
import restful


def run(host, port, ns_host, ns_port):
    """

    Runs the server.

    @param host The host for the server

    @param port The port for the server

    """
    config.app.run(host=host, port=int(port), debug=True, use_reloader=False)
