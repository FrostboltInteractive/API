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
        file.write(f"{data['ip']},{data['port']},{data['status']},{data['region']},{data['playercount']},{nextServerId()}\n")
    # Here you would typically append the new server to your data store
    # For this example, we'll just return the new server
    return {"message": "Server added", "data": data}

def removeServer(data):
    #TODO remove a server from the list
    id = data['id']
    servers = getServerList()
    for i in servers:   
        if(i['id'] == id):
            servers.remove(i)
    with open('/tmp/Servers.txt', 'w') as file:
        for j in range(servers):
            file.write(file.write(f"{servers[j]['ip']},{servers[j]['port']},{servers[j]['status']},{servers[j]['region']},{servers[j]['playercount']},{servers[j]['id']}\n"))
    return "Server #" + str(id) + " removed"

def updateServer(data, newData):
    id = data['id']
    servers = getServerList()
    for i in servers:
        if(i['id'] == id):
            servers[i] = newData
    with open('/tmp/Servers.txt', 'w') as file:
        for j in servers:
            file.write(file.write(f"{servers[j]['ip']},{servers[j]['port']},{servers[j]['status']},{servers[j]['region']},{servers[j]['playercount']},{servers[j]['id']}\n"))
    return ""

def nextServerId():
    servers = getServerList()
    ids = []
    for i in servers:
        ids.append(i['id'])
    for i in range(0, len(ids)):
        if(i not in ids):
            return i
    return len(ids)

def serverNum():
    return len(getServerList())

def getServer(id):
    #TODO get a server by id
    return ""

def startServer():
    #TODO start a server
    return ""

def stopServer(id):
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

def removeMachine(id):
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

@app.route('/removeServer', methods=['POST'])
def handleRemoveServer():
    data = request.get_json()
    res = removeServer(data)
    return Response(json.dumps(res), mimetype='application/json')