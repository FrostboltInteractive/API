from flask import Flask, jsonify
import Endpoints.getServerList as getServerList

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/getServerList')
def handleGetServerList():
    return jsonify(getServerList())