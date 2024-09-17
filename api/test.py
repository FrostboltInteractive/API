from flask import Flask
import Endpoints

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/')
def about():
    return getServerList()