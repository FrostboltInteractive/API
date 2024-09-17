import json

def getServerList():
    #0 = ip
    #1 = port
    #2 = status
    #3 = region
    #4 = playercount
    #5 = id
	servers = [
		{"0.0.0.0", "1", "ok", "usEast", 0, 1}
	]
    #TODO loop to get all servers and set their data in the array
	return json.dumps(servers)

getServerList()