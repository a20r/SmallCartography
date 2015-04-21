
import config
from collections import defaultdict
from flask import request, jsonify
import json


@config.app.route("/join", methods=["POST"])
def post_word_count():
    words = json.loads(request.form["words"])
    super_words = defaultdict(int)
    for word_dict in words:
        for word, num in word_dict.iteritems():
            super_words[word] += num

    return jsonify(super_words)
