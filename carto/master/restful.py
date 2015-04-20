
import config
import uuid
import worker
import grequests
from collections import defaultdict
from flask import request, jsonify


@config.app.route("/beat", methods=["POST"])
def beat():
    try:
        name = request.form["name"]
        config.workers[name].update_time()
        return jsonify(error=0, message="No error")
    except KeyError:
        return jsonify(error=1, message="The worker is not registered")


@config.app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    host = request.form["host"]
    port = request.form["port"]
    w_type = request.form["type"]
    if not name in config.workers:
        wkr = worker.make(name, host, port, w_type)
        config.workers[name] = wkr

        if w_type == worker.WorkerType.MAPPER:
            config.mappers.append(wkr)
        elif w_type == worker.WorkerType.REDUCER:
            config.reducers.append(wkr)

        return jsonify(error=0, message="No error")
    else:
        return jsonify(error=1, message="Worker already registered")


@config.app.route("/destroy", methods=["POST"])
def destroy():
    name = request.form["name"]
    if name in config.workers:
        w_type = config.workers[name].get_type()
        if w_type == worker.WorkerType.MAPPER:
            config.mappers.remove(name)
        elif w_type == worker.WorkerType.REDUCER:
            config.reducers.remove(name)

        return jsonify(error=0, message="No error")
    else:
        return jsonify(error=2, message="The worker has not been registered")


@config.app.route("/worker/<name>", methods=["GET"])
def get_robot(name):
    try:
        wkr = config.workers[name]
        if wkr.still_alive(config.max_time):
            host = wkr.get_host()
            port = wkr.get_port()
            return jsonify(error=0, message="No error", host=host, port=port)
        else:
            return jsonify(error=1, message="The worker is not alive")
    except KeyError:
        return jsonify(error=2, message="The worker has not been registered")


@config.app.route("/count", methods=["POST"])
def post_word_count():
    text = request.form["text"]
    parts = text.split("\n")
    task_id = uuid.uuid4()
    rs = list()
    for i, part in enumerate(parts):
        addr = config.mappers[i % len(config.mappers)].get_address("/count")
        payload = {"id": task_id, "text": part}
        rs.append(grequests.post(addr, data=payload))

    results = grequests.map(rs)
    payloads = [list() for _ in config.reducers]
    for i, res in enumerate(results):
        payloads[i % len(payloads)].append(res.json())

    rs = list()
    for reducer, payload in zip(config.reducers, payloads):
        addr = reducer.get_address("/join")
        rs.append(grequests.post(addr, data=payload))

    results = grequests.map(rs)
    words = defaultdict(int)
    for result in results:
        word_dict = result.json()
        for word, num in word_dict.iteritems():
            words[word] += num

    return jsonify(words)
