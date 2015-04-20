
from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)

mappers = list()
reducers = list()
workers = dict()

# in seconds
max_time = 1 * 60
