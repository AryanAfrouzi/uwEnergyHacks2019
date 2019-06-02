from flask import Flask, request, jsonify
import flask_cors
import greenrouteapi
import google.auth.transport.requests
import requests_toolbelt.adapters.appengine
import logging

requests_toolbelt.adapters.appengine.monkeypatch()
HTTP_REQUEST = google.auth.transport.requests.Request()

app = Flask(__name__)
flask_cors.CORS(app)

@app.route('/api', methods=['POST'])
def algo():
    inp = request.get_json()
    try:
        return jsonify(greenrouteapi.greenroutealgo(inp['location1'], inp['location2'], inp['cartype'])), 200
    except Exception as e:
        logging.CRITICAL(str(e))
        return 'BAD REQUEST', 400
