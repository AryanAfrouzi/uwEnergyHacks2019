from flask import Flask, request, jsonify
import flask_cors
import greenrouteapi
from google.appengine.ext import ndb
import google.auth.transport.requests
import google.oauth2.id_token
import requests_toolbelt.adapters.appengine
import logging
import time

requests_toolbelt.adapters.appengine.monkeypatch()
HTTP_REQUEST = google.auth.transport.requests.Request()

app = Flask(__name__)
flask_cors.CORS(app)

ips = {}

class Account(ndb.Model):
    Midsize_Sedan_CV = ndb.FloatProperty(repeated=True)
    Midsize_Sedan_HEV = ndb.FloatProperty(repeated=True)
    SUV_CV = ndb.FloatProperty(repeated=True)
    SUV_HEV = ndb.FloatProperty(repeated=True)
    created = ndb.DateTimeProperty(auto_now_add=True)

def query_database(user_id):
    ancestor_key = ndb.Key(Account, user_id)
    query = Account.query(ancestor=ancestor_key).order(-Account.created)
    accountData = query.fetch()

    acDataParsed = []
    if len(accountData) > 0:
        accountData = accountData[0]
        acDataParsed.append(accountData)

    return acDataParsed

@app.route('/api', methods=['POST'])
def algo():
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(
    id_token, HTTP_REQUEST)
    if not claims:
        return 'Unauthorized', 401

    entities = query_database(claims['sub'])
    
    if len(entities) != 0:
        data = entities[0]
    else:
        data = Account(
            parent=ndb.Key(Account, claims['sub']),
            Midsize_Sedan_CV=[],
            Midsize_Sedan_HEV=[],
            SUV_CV=[],
            SUV_HEV=[]
            )

    ##
    start = time.time()
    ip = request.remote_addr
    if ip in list(ips.keys()):
        if ips[ip] > time.time():
            return 'RATE LIMIT', 400
    inp = request.get_json()
    #try:
    retval = greenrouteapi.greenroutealgo(inp['location1'], inp['location2'], inp['cartype'])
    if time.time()-start > 1:
        ips[ip] = time.time()+20
    else:
        ips[ip] = time.time()+3
    if inp['cartype'].replace(' ', '_') == 'Midsize_Sedan_CV':
        if len(data.Midsize_Sedan_CV) == 0:
            data.Midsize_Sedan_CV = [retval['carbon'], retval['carbon'], 1, retval['maxcarbonsaved'], retval['maxcarbonsaved'], 1, retval['averagempg'], 1, retval["distancen"], retval["distancen"], 1, retval["distancen"]/retval["timen"]*3600, 1]
        else:
            data.Midsize_Sedan_CV = [data.Midsize_Sedan_CV[0]+retval['carbon'],\
                                        (data.Midsize_Sedan_CV[1]*data.Midsize_Sedan_CV[2]+retval['carbon'])/(data.Midsize_Sedan_CV[2]+1),\
                                        data.Midsize_Sedan_CV[2]+1,\
                                        data.Midsize_Sedan_CV[3]+retval['maxcarbonsaved'],\
                                        (data.Midsize_Sedan_CV[4]*data.Midsize_Sedan_CV[5]+retval['maxcarbonsaved'])/(data.Midsize_Sedan_CV[5]+1),\
                                        data.Midsize_Sedan_CV[5]+1,\
                                        (data.Midsize_Sedan_CV[6]*data.Midsize_Sedan_CV[7]+retval['averagempg'])/(data.Midsize_Sedan_CV[7]+1),\
                                        data.Midsize_Sedan_CV[7]+1,\
                                        data.Midsize_Sedan_CV[8]+retval["distancen"],\
                                        (data.Midsize_Sedan_CV[9]*data.Midsize_Sedan_CV[10]+retval["distancen"])/(data.Midsize_Sedan_CV[10]+1),\
                                        data.Midsize_Sedan_CV[10]+1,\
                                        (data.Midsize_Sedan_CV[11]*data.Midsize_Sedan_CV[12]+retval["distancen"]/retval["timen"]*3600)/(data.Midsize_Sedan_CV[12]+1),\
                                        data.Midsize_Sedan_CV[12]+1]
        data.put()
        return jsonify(retval), 200
    elif inp['cartype'].replace(' ', '_') == 'Midsize_Sedan_HEV':
        if len(data.Midsize_Sedan_HEV) == 0:
            data.Midsize_Sedan_HEV = [retval['carbon'], retval['carbon'], 1, retval['maxcarbonsaved'], retval['maxcarbonsaved'], 1, retval['averagempg'], 1, retval["distancen"], retval["distancen"], 1, retval["distancen"]/retval["timen"]*3600, 1]
        else:
            data.Midsize_Sedan_HEV = [data.Midsize_Sedan_HEV[0]+retval['carbon'],\
                                        (data.Midsize_Sedan_HEV[1]*data.Midsize_Sedan_HEV[2]+retval['carbon'])/(data.Midsize_Sedan_HEV[2]+1),\
                                        data.Midsize_Sedan_HEV[2]+1,\
                                        data.Midsize_Sedan_HEV[3]+retval['maxcarbonsaved'],\
                                        (data.Midsize_Sedan_HEV[4]*data.Midsize_Sedan_HEV[5]+retval['maxcarbonsaved'])/(data.Midsize_Sedan_HEV[5]+1),\
                                        data.Midsize_Sedan_HEV[5]+1,\
                                        (data.Midsize_Sedan_HEV[6]*data.Midsize_Sedan_HEV[7]+retval['averagempg'])/(data.Midsize_Sedan_HEV[7]+1),\
                                        data.Midsize_Sedan_HEV[7]+1,\
                                        data.Midsize_Sedan_HEV[8]+retval["distancen"],\
                                        (data.Midsize_Sedan_HEV[9]*data.Midsize_Sedan_HEV[10]+retval["distancen"])/(data.Midsize_Sedan_HEV[10]+1),\
                                        data.Midsize_Sedan_HEV[10]+1,\
                                        (data.Midsize_Sedan_HEV[11]*data.Midsize_Sedan_HEV[12]+retval["distancen"]/retval["timen"]*3600)/(data.Midsize_Sedan_HEV[12]+1),\
                                        data.Midsize_Sedan_HEV[12]+1]
        data.put()
        return jsonify(retval), 200
    elif inp['cartype'].replace(' ', '_') == 'SUV_CV':
        if len(data.SUV_CV) == 0:
            data.SUV_CV = [retval['carbon'], retval['carbon'], 1, retval['maxcarbonsaved'], retval['maxcarbonsaved'], 1, retval['averagempg'], 1, retval["distancen"], retval["distancen"], 1, retval["distancen"]/retval["timen"]*3600, 1]
        else:
            data.SUV_CV = [data.SUV_CV[0]+retval['carbon'],\
                                        (data.SUV_CV[1]*data.SUV_CV[2]+retval['carbon'])/(data.SUV_CV[2]+1),\
                                        data.SUV_CV[2]+1,\
                                        data.SUV_CV[3]+retval['maxcarbonsaved'],\
                                        (data.SUV_CV[4]*data.SUV_CV[5]+retval['maxcarbonsaved'])/(data.SUV_CV[5]+1),\
                                        data.SUV_CV[5]+1,\
                                        (data.SUV_CV[6]*data.SUV_CV[7]+retval['averagempg'])/(data.SUV_CV[7]+1),\
                                        data.SUV_CV[7]+1,\
                                        data.SUV_CV[8]+retval["distancen"],\
                                        (data.SUV_CV[9]*data.SUV_CV[10]+retval["distancen"])/(data.SUV_CV[10]+1),\
                                        data.SUV_CV[10]+1,\
                                        (data.SUV_CV[11]*data.SUV_CV[12]+retval["distancen"]/retval["timen"]*3600)/(data.SUV_CV[12]+1),\
                                        data.SUV_CV[12]+1]
        data.put()
        return jsonify(retval), 200
    elif inp['cartype'].replace(' ', '_') == 'SUV_HEV':
        if len(data.SUV_HEV) == 0:
            data.SUV_HEV = [retval['carbon'], retval['carbon'], 1, retval['maxcarbonsaved'], retval['maxcarbonsaved'], 1, retval['averagempg'], 1, retval["distancen"], retval["distancen"], 1, retval["distancen"]/retval["timen"]*3600, 1]
        else:
            data.SUV_HEV = [data.SUV_HEV[0]+retval['carbon'],\
                                        (data.SUV_HEV[1]*data.SUV_HEV[2]+retval['carbon'])/(data.SUV_HEV[2]+1),\
                                        data.SUV_HEV[2]+1,\
                                        data.SUV_HEV[3]+retval['maxcarbonsaved'],\
                                        (data.SUV_HEV[4]*data.SUV_HEV[5]+retval['maxcarbonsaved'])/(data.SUV_HEV[5]+1),\
                                        data.SUV_HEV[5]+1,\
                                        (data.SUV_HEV[6]*data.SUV_HEV[7]+retval['averagempg'])/(data.SUV_HEV[7]+1),\
                                        data.SUV_HEV[7]+1,\
                                        data.SUV_HEV[8]+retval["distancen"],\
                                        (data.SUV_HEV[9]*data.SUV_HEV[10]+retval["distancen"])/(data.SUV_HEV[10]+1),\
                                        data.SUV_HEV[10]+1,\
                                        (data.SUV_HEV[11]*data.SUV_HEV[12]+retval["distancen"]/retval["timen"]*3600)/(data.SUV_HEV[12]+1),\
                                        data.SUV_HEV[12]+1]
        data.put()
        return jsonify(retval), 200
    #except Exception as e:
    #    logging.info(e)
    #    return 'BAD REQUEST', 400
    ##

        
@app.route('/api', methods=['GET'])
def algog():
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(
    id_token, HTTP_REQUEST)
    if not claims:
        return 'Unauthorized', 401

    entities = query_database(claims['sub'])
    
    if len(entities) != 0:
        return jsonify([entities[0].Midsize_Sedan_CV, entities[0].Midsize_Sedan_HEV, entities[0].SUV_CV, entities[0].SUV_HEV]), 200
    else:
        return jsonify([]), 200
    
