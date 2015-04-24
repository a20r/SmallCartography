
import re
import config
import json
import random
from flask import request
from collections import Counter


@config.app.route("/count", methods=["POST"])
def post_word_count():
    if random.random() > config.CRASH_PROB:
        text = request.form["text"]
        map_id = request.form["map_id"]
        text_hash = request.form["hash"]
        if int(text_hash) != hash(text):
            return

        words = Counter(re.findall("\w+", text.lower()))
        return json.dumps({
            "words": words, "map_id": map_id})
    else:
        shutdown_server()


@config.app.route("/kill")
def kill_worker():
    shutdown_server()
    return "Shut down server"


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
