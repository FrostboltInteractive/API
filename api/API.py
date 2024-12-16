from flask import Flask, Response, request, jsonify 
import json
import os
import redis
import requests

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
    s = f"{data['ip']},{data['port']},{data['status']},{data['region']},{data['playerCount']},{data['shipCount']},{nextServerId()},{data['machineID']},{data['connectedPlayers']}\n"
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

def startServer():
    #TODO start a server
    least = leastLoadedMachine()
    machineURL = f"http://{least['ip']}:{least['port']}/startServer"
    try:
        response = request.get(machineURL)
        return response.content
    except Exception as e:  
        return str(e)
    return "FAIL"

def stopServer(id):
    #TODO stop a server
    return ""

def getMachineList():
    data = dataGet("Machines")
    machines = [] 
    mac = data.split('\n')
    if(type(mac) == str):
        mac = [mac]
    else:
        mac = mac
    
    for line in mac:
        print(type(line))
        arr = line.split(',')
        if(len(arr) < 7):
            continue
        else:   
            print("Test")
            strs = line.strip().split(',')
            ip = strs[0]
            port = strs[1]
            region = strs[2]
            serverCount = strs[3]
            status = strs[4]
            id = strs[5]
            serverIds = strs[6]
            serverIds = serverIds.split('&')
            machines.append({
                "ip": ip,
                "port": port,
                "region": region,
                "serverCount": int(serverCount),
                "status": status,
                "id": int(id),
                "serverIds": serverIds
            })
    return machines

def leastLoadedMachine():
    machines = getMachineList()
    min = machines[0]
    for mac in machines:
        if(mac.serverCount < min.serverCount):
            min = mac
    return min

def addMachine(data):
    #1: ip
    #2: port
    #3: region
    #4: serverCount
    #5: status
    #6: id
    #7: serverIds (list) format = 1&2&3&4
    #TODO add a machine
    serverIds = data['serverIds']
    ids_list = []
    servers = getServerList()
    if(servers != None):
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
    olddata = dataGet("Machines")
    s = f"{data['ip']},{data['port']},{data['region']},{data['serverCount']},{data['status']},{id},{ids}\n"
    dataStore("Machines", olddata + s)
    
    # Return the response
    return "Machine Added ID: " + str(id)

def getNextMachineId():
    machines = getMachineList()
    if(machines == None):
        return 0
    ids = []
    for i in machines:
        ids.append(i['id'])
    for i in range(0, len(ids)):
        if(i not in ids):
            return i
    return len(ids)

def wipeMachineList():
    dataStore("Machines", "")
    return "Machine list wiped"

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
        print(val)
        return val.decode('utf-8')  # Decode bytes to string
    return None

def findServer(region, ip):
    servers = getServerList()
    filt = []
    for i in servers:
        if(i['region'] == region & i['playerCount'] < 10):
            filt.append(i)
    if(len(filt) == 0):
        #start new server
        res = startServer()
        #return the new server
        return res 
    #have all eligable servers ping the client
    pings = []
    for server in filt:
        response = requests.get("http://" + server['ip'] + ":" + server['port'] + "/ping")
        pings[server['id']] = response.content
        print(response.content)
    #return the server with the lowest ping
    print(pings)
    m = 0
    for i in pings:
        if(pings[i] < pings[m]):
            m = i
    return servers[m]


app = Flask(__name__)

@app.route('/test')
def test():
    return "Hello, World!"

@app.route('/connect', methods=['POST'])
def handleConnect():
    data = request.get_json()
    #step 1 have all servers in the same region and arent full ping the client and the one with the lowest ping will be the chosen server
    server = findServer("USEAST", data['ip'])
    #step 2 send client the ip and port of the chosen server
    return server['ip'] + ":" + server['port']  

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

@app.route('/serverHeartBeat', methods=['POST'])
def handleServerHeartBeat():
    data = request.get_json()
    #TODO handle server heartbeat
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

@app.route('/mtest', methods=['POST'])
def handleMTest():
    data = request.get_json()
    print("requesting")
    response = requests.get("http://" + data['ip'] + ":" + data['port'] + "/test")
    print(response.content)
    return "successapi"

@app.route('/wipeMachineList', methods=['GET'])
def handleWipeMachineList():
    res = wipeMachineList()
    return Response(json.dumps(res), mimetype='application/json')

@app.route('/setDB', methods=['POST'])
def handleSetDB():
    data = request.get_json()
    return "not implemented"