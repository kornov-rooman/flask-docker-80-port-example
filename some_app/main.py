import socket

import flask
import requests

app = flask.Flask(__name__)


@app.route('/hostname')
def hostname():
    return flask.jsonify(hostname=socket.gethostname())


@app.route('/ping')
def ping():
    return flask.jsonify(pong=True)


@app.route('/ask_hostname')
def ask_hostname():
    queries = flask.request.args.copy()

    if 'url' in queries:
        url = 'http://%s/hostname' % queries['url']
        response = requests.get(url)

        if response.status_code == 200:
            return flask.jsonify(his_name=response.json().get('hostname', 'unknown'))

    return flask.jsonify(idk=None)
