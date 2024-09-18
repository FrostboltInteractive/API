from flask import Flask, Response, request
import json
from flask_cors import CORS


#Endpoints
def getServerList():
    #0 = ip
    #1 = port
    #2 = status
    #3 = region
    #4 = playercount
    #5 = id
    servers = [
        {"ip": "0.0.0.0", "port": 1, "status": "ok", "region": "usEast", "playercount": 0, "id": 1}
    ]
    #TODO loop to get all servers and set their data in the array
    return servers

def addServer(data):
    
    return ""

def removeServer():
    #TODO remove a server from the list
    return ""

def updateServer():
    #TODO update the server data
    return ""

def getServer():
    #TODO get a server by id
    return ""

def startServer():
    #TODO start a server
    return ""

def stopServer():
    #TODO stop a server
    return ""

def getMachines():
    #TODO get all machines
    return ""

def leastLoadedMachine():
    #TODO get the machine with the least amount of servers
    return ""

def addMachine():
    #TODO add a machine
    return ""

def removeMachine():
    #TODO remove a machine
    return ""


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://oceansedge.frostboltinteractive.com"}})  # Enable CORS for the specified origin

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/getServerList')
def handleGetServerList():
    res = list(getServerList())
    return Response(json.dumps(res), mimetype='application/json')

@app.route('/addServer', methods=['POST'])
def handleAddServer():
    data = request.get_json()  # Get the JSON data from the POST request
    res = addServer(data)
    return Response(json.dumps(res), mimetype='application/json')
