# this is what the game servers and clients are going to interact with for matchmaking and this will controll all of the game servers
# manages all the servers and their status if there are no open servers in a region then it will open a new server on the machine with the least resources used
# it will also close servers that are not being used
# it will also update the status of the servers and the server list every 5 minutes
# manages database 
# hosts a server that when connected with will recive 6 possible requests 
# 1. getServerList - returns a list of all the servers ips and their status
# 2. getServer - returns a specific servers ip and port
# 3. anyOpenServers - checks if there are any open servers in a region if returns false then it will open a new server in that region
# 4. getLoginData - returns the login data of the user
# 5. getServerData - returns the server data of the user
# 6. setServerData - sets some data based on what is requested

import json
from flask import Flask, request, jsonify
from api import getServerList, updateIP
#server management stuff

#api stuff
app = Flask(__name__)

@app.route('/api/getServerList', methods=['GET'])
def handleGetServerList():
    server_list = getServerList()
    return jsonify(json.loads(server_list))

@app.route('/api/updateIP', methods=['GET']) 
def handleUpdateIP():
	return updateIP()