from flask import Flask, Response, request, jsonify 
import json
import os
import redis

redis_url = os.getenv('REDIS_URL')

# Create a Redis client
redis_client = redis.Redis.from_url(redis_url)#Endpoints
def getServerList():
    servers = []
    # Get the absolute path of the current file
    dat = dataGet("Servers")
    if dat is None:
        return []
    arr = dat.split('\n')
    for line in arr:
        line = str(line)
        arr = line.split(',')
        if(len(arr) < 8):
            continue
        else:
            ip = arr[0]
            port = arr[1]
            status = arr[2]
            region = arr[3]
            playerCount = arr[4]
            shipCount = arr[5]
            serverID = arr[6]
            machineID = arr[7]
            servers.append({
                "ip": ip,
                "port": int(port),
                "status": status,
                "region": region,
                "playerCount": int(playerCount),
                "shipCount": int(shipCount),
                "serverID": int(serverID),
                "machineID": int(machineID)
            })
    return servers


def addServer(data):
    # Example logic to add the server to the list
    serv = dataGet("Servers")
    if(serv is None):
        serv = ""
    s = f"{data['ip']},{data['port']},{data['status']},{data['region']},{data['playerCount']},{data['shipCount']},{nextServerId()},{data['machineID']}\n"
    dataStore("Servers", serv + s)
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
        for j in range(len(servers)):
            file.write(f"{servers[j]['ip']},{servers[j]['port']},{servers[j]['status']},{servers[j]['region']},{servers[j]['playerCount']},{servers[j]['id']}\n")
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
        ids.append(i['serverID'])
    for i in range(0, len(ids)):
        if(i not in ids):
            return i
    return len(ids)

def serverNum():
    return len(getServerList())

def getServer(id):
    #TODO get a server by id
    return ""

def startServer(machineID):
    #TODO start a server
    least = leastLoadedMachine()
    machineIP = "192.168.1.100"  # Replace with the actual IP address of the Java server
    machinePort = 8080
    machineURL = f"http://{machineIP}:{machinePort}/startServer"
    try:
        response = request.get(machineURL)
        return response.text
    except Exception as e:  
        return str(e)
    return "FAIL"

def stopServer(id):
    #TODO stop a server
    return ""

def getMachineList():
    machines= []
    data = dataGet("Machines")
    for line in data:
        arr = line.split(',')
        if(len(arr) < 6):
            continue
        else:
            strs = line.strip().split(',')
            ip = strs[0]
            region = strs[1]
            serverCount = strs[2]
            status = strs[3]
            id = strs[4]
            serverIds = strs[5]
            serverIds = serverIds.split('&')
            machines.append({
                "ip": ip,
                "region": region,
                "serverCount": int(serverCount),
                "status": status,
                "id": int(id),
                "serverIds": serverIds
            })
    return machines

def leastLoadedMachine():
    #TODO get the machine with the least amount of servers
    return ""

def addMachine(data):
    #1: ip
    #2: region
    #3: serverCount
    #4: status
    #5: id
    #6: serverIds (list) format = 1&2&3&4
    #TODO add a machine
    serverIds = data['serverIds']
    ids_list = []
    servers = getServerList()
    
    # Loop through the servers and check the type
    for server in servers:
        if isinstance(server, dict):  # Ensure server is a dictionary
            if server.get('serverID') in serverIds:
                ids_list.append(str(server['serverID']))
        else:
            print(f"Unexpected server type: {type(server)} - {server}")
    
    # Join the collected IDs with '&'
    ids = "&".join(ids_list)
    print(ids)
    id = getNextMachineId()
    # Write to file
    s = f"{data['ip']},{data['region']},{data['serverCount']},{data['status']},{id},{ids}\n"
    dataStore("Machines", s)
    
    # Return the response
    return "Machine Added ID: " + str(id)

def getNextMachineId():
    machines = getMachineList()
    ids = []
    for i in machines:
        ids.append(i['machineID'])
    for i in range(0, len(ids)):
        if(i not in ids):
            return i
    return len(ids)

def getMachineIp(id):
    #TODO get the ip of a machine

    return ""

def removeMachine(id):
    #TODO remove a machine
    return ""

def clearMachine():
    with open('/tmp/Servers.txt', 'w') as file:
        file.write("")
    
def dataStore(key, val): #takes in json and stores it in redis
    redis_client.set(key, val)

def dataGet(key): #takes in key and returns the value from redis
    val = redis_client.get(key)
    if val is not None:
        return val.decode('utf-8')  # Decode bytes to string
    return None


app = Flask(__name__)

@app.route('/test')
def test():
    dataStore("servers", "127.0.0.1,5500,running,USEAST,10,5,0,0")
    return dataGet("servers")

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

@app.route('/updateServer', methods=['POST'])
def handleUpdateServer():
    newData = request.get_json()
    data = newData['id']
    res = updateServer(data, newData)
    return Response(json.dumps(res), mimetype='application/json')

@app.route('/machineHeartbeat', methods=['POST'])
def handleMachineHeartbeat():
    data = request.get_json()
    #TODO handle machine heartbeat
    return ""

@app.route('/addMachine', methods=['POST']) 
def handleAddMachine():
    data = request.get_json()
    res = addMachine(data)
    return Response(json.dumps(res), mimetype='application/json')

@app.route('/getMachineList', methods=['GET'])
def handleGetMachineList():
    res = getMachineList()
    return Response(json.dumps(res), mimetype='application/json')

@app.route('/getMachineIp', methods=['GET'])
def handleGetMachineIp():
    data = request.get_json()
    res = getMachineIp(data)
    return Response(json.dumps(res), mimetype='application/json')

