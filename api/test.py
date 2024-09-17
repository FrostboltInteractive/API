from flask import Flask, jsonify
from getServerList import getServerList  # Correct import


app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/getServerList')
def handleGetServerList():
    return jsonify(getServerList())