from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
servers = [
    {"ip": "0.0.0.0", "port": "1", "status": "ok", "region": "usEast", "playercount": 0, "id": 1}
]

@app.route('/getServerList', methods=['GET'])
def get_server_list():
    return jsonify(servers)

@app.route('/addServer', methods=['POST'])
def add_server():
    new_server = request.get_json()
    servers.append(new_server)
    return jsonify(new_server), 201

@app.route('/getServer/<int:server_id>', methods=['GET'])
def get_server(server_id):
    server = next((s for s in servers if s["id"] == server_id), None)
    if server:
        return jsonify(server)
    else:
        return jsonify({"error": "Server not found"}), 404

@app.route('/updateServer/<int:server_id>', methods=['PUT'])
def update_server(server_id):
    server = next((s for s in servers if s["id"] == server_id), None)
    if server:
        data = request.get_json()
        server.update(data)
        return jsonify(server)
    else:
        return jsonify({"error": "Server not found"}), 404

@app.route('/deleteServer/<int:server_id>', methods=['DELETE'])
def delete_server(server_id):
    global servers
    servers = [s for s in servers if s["id"] != server_id]
    return jsonify({"message": "Server deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)