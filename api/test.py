from flask import Flask, Response
import json
from servers import getServerList


app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/getServerList')
def handleGetServerList():
    res = list(getServerList())
    return Response(json.dumps(res), mimetype='application/json')

