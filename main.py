from flask import Flask, request, jsonify
import flask_cors
import greenrouteapi
import google.auth.transport.requests
import requests_toolbelt.adapters.appengine
import logging
import time

requests_toolbelt.adapters.appengine.monkeypatch()
HTTP_REQUEST = google.auth.transport.requests.Request()

app = Flask(__name__)
flask_cors.CORS(app)

ips = {}

@app.route('/api', methods=['POST'])
def algo():
    start = time.time()
    ip = request.remote_addr
    if ip in list(ips.keys()):
        if ips[ip] > time.time():
            return 'RATE LIMIT', 400
    inp = request.get_json()
    try:
        retval = jsonify(greenrouteapi.greenroutealgo(inp['location1'], inp['location2'], inp['cartype']))
        if time.time()-start > 1:
            ips[ip] = time.time()+20
        else:
            ips[ip] = time.time()+3
        return retval, 200
    except Exception as e:
        logging.info(e)
        return 'BAD REQUEST', 400
