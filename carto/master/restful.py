
import config
import worker
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
    wkr = worker.make(name, host, port, w_type)
    config.workers[name] = wkr

    if w_type == worker.WorkerType.MAPPER:
        config.mappers.add(wkr)
    elif w_type == worker.WorkerType.REDUCER:
        config.reducers.add(name)

    return jsonify(error=0, message="No error")


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
    return text
