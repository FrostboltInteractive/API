from flask import Flask, Response
import json
#from getServerList import getServerList  # Correct import

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
	return servers


app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/getServerList')
def handleGetServerList():
    res = list(getServerList())
    return Response(json.dumps(res), mimetype='application/json')

