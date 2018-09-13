#!/usr/bin/env python3

from flask import Flask, jsonify, request
import threading
import time
import os
from functools import partial
from config import config
from multiprocessing.dummy import Pool as ThreadPool
import requests
import os
import sys
from itertools import product

app = Flask(__name__)

local_data_storage = {}
local_data_storage['data'] = {}
port1 = sys.argv[1]

# For only testing, use pkill python and restart kvstore_start_script to clean all instances
@app.route('/clear', methods=['GET'])
def clear():
        local_data_storage['data'] = {}
        return jsonify(local_data_storage)


@app.route('/get', methods=['GET'])
def get():
    return jsonify(local_data_storage)


@app.route('/get/<name>', methods=['GET'])
def get_name(name):
    print("Process {}".format(os.getpid()))
    return jsonify(local_data_storage['data'].get(name, {}))


@app.route('/setinternal/<name>', methods=['GET', 'POST'])
def setinternal(name):
    global local_data_storage
    local_data_storage['data'][name] = local_data_storage['data'].get(name, {})
    local_data_storage['data'][name]['value'] = request.args.get('value') or float('nan')
    local_data_storage['data'][name]['time'] = time.time()
    return jsonify(local_data_storage)


@app.route('/setkey/<name>', methods=['GET', 'POST'])
def setkey(name):
    global local_data_storage
    local_data_storage['data'][name] = local_data_storage['data'].get(name, {})
    local_data_storage['data'][name]['value'] = request.args.get('value') or float('nan')
    local_data_storage['data'][name]['time'] = time.time()
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
    return jsonify(local_data_storage['data'].get(name, {}))


if __name__ == '__main__':
    app.run(port=sys.argv[1])