
from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)

mappers = dict()
reducers = dict()
workers = dict()

# in minutes
max_beat_time = 1 * 60
