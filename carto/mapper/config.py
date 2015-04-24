
from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)

OMISSION_PROB = 0.1
CRASH_PROB = 0.1
