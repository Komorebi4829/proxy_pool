import os
import sys
import random
from flask import Flask, request, jsonify

import config
from proxy_pool import ProxyPool

app = Flask(__name__)


@app.route('/')
def index():
    return 'Proxy Pool'


@app.route('/get')
def get():
    p = ProxyPool.get()
    return p


@app.route('/count')
def count():
    n = ProxyPool.count()
    return str(n)


@app.route('/delete')
def delete():
    pass
    return 'not complete'


application = app


def run():
    app.run(host=config.web_host, port=config.web_port)


if __name__ == '__main__':
    run()
