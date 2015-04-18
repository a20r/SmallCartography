
import config
import worker
import time
from flask import request, jsonify


@config.app.route("/beat", methods=["POST"])
def beat():
    name = request.form["name"]
    config.alive_table[name] = time.time()
    return jsonify(error=0, message="No error")


@config.app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    host = request.form["host"]
    port = request.form["port"]
    w_type = request.form["port"]
    config.workers[name] = worker.make(name, host, port, w_type)
    return jsonify(error=0, message="No error")


@config.app.route("/destroy", methods=["POST"])
def destroy():
    name = request.form["name"]
    del config.alive_table[name]
    del config.server_table[name]
    return jsonify(error=0, message="No error")


@config.app.route("/robot/<name>", methods=["GET"])
def get_robot(name):
    try:
        if time.time() - config.alive_table[name] < config.max_beat_time:
            host, port = config.server_table[name]
            return jsonify(error=0, message="No error", host=host, port=port)
        else:
            return jsonify(error=1, message="The robot is not alive")
    except KeyError:
        return jsonify(error=2, message="The robot has not been registered")


@config.app.route("/alive", methods=["GET"])
def get_all_alive():
    alive_list = list()
    for name, t in config.alive_table.iteritems():
        if time.time() - t < config.max_beat_time:
            alive_list.append(name)

    return jsonify(error=0, message="No error", alive=alive_list)


@config.app.route("/alive/<name>", methods=["GET"])
def get_alive(name):
    try:
        if time.time() - config.alive_table[name] < config.max_beat_time:
            return jsonify(error=0, message="No error", alive=True)
        else:
            return jsonify(error=0, message="No error", alive=False)
    except KeyError:
        return jsonify(error=2, message="The robot has not been registered")
