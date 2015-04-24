
import config
import uuid
import worker
import grequests
from collections import defaultdict
from flask import request, jsonify
import json


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


def get_mappers():
    mappers = list()
    for mapper in config.mappers:
        wkr = config.workers[mapper.get_name()]
        if wkr.still_alive(config.max_time):
            mappers.append(wkr)
    return mappers


def get_reducers():
    reducers = list()
    for reducer in config.reducers:
        wkr = config.workers[reducer.get_name()]
        if wkr.still_alive(config.max_time):
            reducers.append(wkr)
    return reducers


def chunks(text, num):
    parts = text.split("\n")
    prtn = len(parts) / num
    # print "portinos", prtn
    for i in xrange(num):
        if i < num - 1:
            yield " ".join(p for p in parts[i * prtn:prtn * (i + 1)])
        else:
            yield " ".join(p for p in parts[i * prtn:])


def map_task(text, task_id):
    mappers = get_mappers()
    map_ids = set()
    rs = list()
    payloads = list()
    for i, part in enumerate(chunks(text, len(mappers))):
        addr = mappers[i].get_address("/count")
        payload = {
            "id": task_id,
            "map_id": i,
            "hash": hash(part),
            "text": part}
        payloads.append(payload)
        rs.append(grequests.post(addr, timeout=1, data=payload))
        map_ids.add(str(i))

    results = grequests.map(rs)
    total_results = results
    ret_ids = set()
    good_mappers = list()
    for result in results:
        ret_ids.add(result.json()["map_id"])
        good_mappers.append(int(result.json()["map_id"]))

    while len(map_ids - ret_ids) > 0:
        rs = list()
        cmi = 0
        mapper_mapping = dict()

        for i in map_ids - ret_ids:
            payload = payloads[int(i)]
            good_map_id = good_mappers[cmi % len(good_mappers)]
            mapper_mapping[good_map_id] = int(payload["map_id"])
            addr = mappers[good_map_id].get_address("/count")
            rs.append(grequests.post(addr, timeout=1, data=payload))
            cmi += 1

        resend_results = grequests.map(rs)
        fulfilled_reqs = set()
        for res in resend_results:
            ret_ids.add(res.json()["map_id"])
            total_results.append(res)
            fulfilled_reqs.add(int(res.json()["map_id"]))

        for good_mapper_id in mapper_mapping:
            if not mapper_mapping[good_mapper_id] in fulfilled_reqs:
                good_mappers.remove(good_mapper_id)

    return total_results


def reduce_task(results):
    reducers = get_reducers()
    payloads = list()
    word_payloads = [list() for _ in reducers]
    map_ids = set()
    for i, res in enumerate(results):
        word_payloads[i % len(word_payloads)].append(res.json()["words"])

    rs = list()
    red_id = 0
    for reducer, payload in zip(reducers, word_payloads):
        addr = reducer.get_address("/join")
        data = {"words": json.dumps(payload), "red_id": red_id}
        payloads.append(data)
        rs.append(grequests.post(addr, timeout=1, data=data))
        map_ids.add(red_id)
        red_id += 1

    return grequests.map(rs)


def master_reduce(results):
    words = defaultdict(int)
    for result in results:
        word_dict = result.json()["words"]
        for word, num in word_dict.iteritems():
            words[word] += num
    return words


@config.app.route("/count", methods=["POST"])
def post_word_count():
    text = request.form["text"]
    task_id = uuid.uuid4()
    map_results = map_task(text, task_id)
    reduce_results = reduce_task(map_results)
    words = master_reduce(reduce_results)
    return jsonify(words)


@config.app.route("/kill")
def kill_all():
    rs = list()
    for worker in config.workers.values():
        addr = worker.get_address("/kill")
        rs.append(grequests.get(addr))

    grequests.map(rs)
    shutdown_server()
    return "Server is dead my friend"


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
