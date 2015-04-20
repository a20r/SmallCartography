
import config
from collections import defaultdict
from flask import request, jsonify


@config.app.route("/join", methods=["POST"])
def post_word_count():
    words = request.form["words"]
    # task_id = request.form["id"]
    super_words = defaultdict(int)
    print words
    for word_dict in words:
        for word, num in word_dict.iteritems():
            super_words[word] += num

    return jsonify(super_words)
