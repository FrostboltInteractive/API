from flask import Flask
from Endpoints import getServerList

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/')
def about():
    return getServerList()