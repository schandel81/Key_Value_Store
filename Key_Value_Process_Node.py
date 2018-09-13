#!/usr/bin/env python3

from flask import Flask, jsonify, request
import threading
import time
import os
from functools import partial
import config
from multiprocessing.dummy import Pool as ThreadPool
import requests
import os
import sys
from itertools import product

# Set key "field1": http://localhost:5000/set/field1?value=42
# Get key "field1": http://localhost:5000/get/field1
# Get all :         http://localhost:5000/get
# Clear all :       http://localhost:5000/clear

app = Flask(__name__)

d = {}
d['data'] = {}
port1 = sys.argv[1]


def print_func(p1):
    print("Process {} got message {}".format(os.getpid(), p1))


@app.route('/clear', methods=['GET'])
def clear():
        d['data'] = {}
        return jsonify(d)


@app.route('/get', methods=['GET'])
def get():
    return jsonify(d)


@app.route('/get/<name>', methods=['GET'])
def get_name(name):
    print("Process {}".format(os.getpid()))
    return jsonify(d['data'].get(name, {}))


@app.route('/setinternal/<name>', methods=['GET', 'POST'])
def setinternal(name):
    global d
    d['data'][name] = d['data'].get(name, {})
    d['data'][name]['value'] = request.args.get('value') or float('nan')
    d['data'][name]['time'] = time.time()
    return jsonify(d)


@app.route('/setkey/<name>', methods=['GET', 'POST'])
def setkey(name):
    global d
    d['data'][name] = d['data'].get(name, {})
    d['data'][name]['value'] = request.args.get('value') or float('nan')
    d['data'][name]['time'] = time.time()
    for x in range(4):
        ip, port = config['hosts'][x]
        if str(port) == str(port1):
            print("Host ip Address {} and port is {}".format(ip, port))
            continue
        try:
            r = requests.get('http://{}:{}/setinternal/{}?value={}'.format(ip, port, name, request.args.get('value') or float('nan')))
            print("Sync Status on {} is {}".format(port, r.status_code))
        except Exception as e:
            print(str(e))
    return jsonify(d)


if __name__ == '__main__':
    app.run(port=sys.argv[1])