import json
import socket

def getServerList():
	servers = [
		
	]
	return json.dumps(servers)

def updateIP():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip