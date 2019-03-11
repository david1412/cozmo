#!/usr/bin/env python3
from flask import Flask
from observable import Observable
app = Flask(__name__)
_obs = None

@app.route('/drive')
def index():
    dist = request.args.get('dist')
    print("dist: ", dist)
    _obs.trigger("drive", dist)
    return ""

@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return "Server shutting down..."

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def run(obs: Observable):
    global _obs
    _obs = obs
    _obs.trigger("init", "Init Web")
    app.run(debug=False)
    print("Web stopped!!!")
