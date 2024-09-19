from flask import Flask, Response, request
import json
import os

#Endpoints
def getServerList():
    servers = []
    # Get the absolute path of the current file
    current_dir = os.path.dirname(os.path.realpath(__file__))
    
    # Construct the absolute path to the Servers.txt file
    file_path = os.path.join(current_dir, '/tmp/Servers.txt')
    try:
        with open(file_path, 'r') as file:
            for line in file:
                ip, port, status, region, playercount, id = line.strip().split(',')
                servers.append({
                    "ip": ip,
                    "port": int(port),
                    "status": status,
                    "region": region,
                    "playercount": int(playercount),
                    "id": int(id)
                })
    except FileNotFoundError:
        return {"error": "FUCK"}
    
    return servers

def addServer(data):
    # Example logic to add the server to the list
    file_path = '/tmp/Servers.txt'
    with open(file_path, 'a') as file:
        file.write(f"{data['ip']},{data['port']},{data['status']},{data['region']},{data['playercount']},{data['id']}\n")
    # Here you would typically append the new server to your data store
    # For this example, we'll just return the new server
    return {"message": "Server added", "data": data}

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

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/getServerList')
def handleGetServerList():
    res = getServerList()
    return Response(json.dumps(res), mimetype='application/json')


@app.route('/addServer', methods=['POST'])
def handleAddServer():
    data = request.get_json()
    res = addServer(data)
    return Response(json.dumps(res), mimetype='application/json')
