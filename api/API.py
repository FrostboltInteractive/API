from flask import Flask, Response
import json

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

def addServer():
    #TODO add a server to the list
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



app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/getServerList')
def handleGetServerList():
    res = list(getServerList())
    return Response(json.dumps(res), mimetype='application/json')

