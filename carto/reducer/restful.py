
import config
from collections import defaultdict
from flask import request
import json
import random


@config.app.route("/join", methods=["POST"])
def post_word_count():
    words = json.loads(request.form["words"])
    red_id = request.form["red_id"]
    super_words = defaultdict(int)
    for word_dict in words:
        for word, num in word_dict.iteritems():
            super_words[word] += num

    return json.dumps({"words": super_words, "red_id": red_id})


@config.app.route("/kill")
def kill_worker():
    shutdown_server()
    return "Shut down server"


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
