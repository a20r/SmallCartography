
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import carto
import pprint


def count_test():
    filename = "texts/hamlet.txt"
    host = "localhost"
    port = 8080
    ms = carto.client.MasterStub(host, port)
    return ms.count(filename)


if __name__ == "__main__":
    pprint.pprint(count_test())
