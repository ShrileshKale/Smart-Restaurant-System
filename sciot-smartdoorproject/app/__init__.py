from flask import Flask, render_template
from flask_mongokit import MongoKit
from flask_socketio import SocketIO, emit, send, join_room
import json
from bson import json_util
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.config.from_object('conf.mainconf.DevelopmentConfig')

db = MongoKit(app)

import api