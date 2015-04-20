
import config
from flask import request, jsonify


@config.app.route("/count", methods=["POST"])
def post_word_count():
    text = request.form["text"]
    task_id = request.form["id"]
    word_dict = dict()
    for word in text.split():
        if not word in word_dict:
            word_dict[word] = 0
        word_dict[word] += 1
    return jsonify(word_dict)
