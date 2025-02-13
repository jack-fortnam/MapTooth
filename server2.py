from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
import pickle
import socket

# Flask setup
app = Flask(__name__)
socketio = SocketIO(app)

# Constants and storage
api_key = "VPB535HB"
locations = {}
IP = socket.gethostbyname(socket.gethostname())

# Routes for HTML templates
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/node', methods=['GET'])
def node():
    return render_template('node.html')

@app.route('/submitted', methods=['POST'])
def submitted():
    data = request.form
    nodeId = data['nodeID']
    nodeName = data['nodeName']
    what3 = data['w3w']
    with open('locations.txt', 'a') as f:
        f.write(f"\n{nodeId},{nodeName},{what3}")
    return render_template('node.html', submitted=f"Node Submitted :D {nodeId} {nodeName} {what3}")

# REST API for device locations
@app.route('/locations', methods=['GET'])
def get_locations():
    return jsonify(locations)

# WebSocket handling
@socketio.on('report_in')
def handle_report_in(data):
    report = pickle.loads(data)
    device_id = f"{report[0]}"
    detected_devices = report[1:]
    locations[device_id] = detected_devices
    print(f"Updated locations: {locations}")

# Main driver function
if __name__ == '__main__':
    print(f"Server online at {IP}:5000 and WebSocket active")
    socketio.run(app, host='0.0.0.0', port=5000,allow_unsafe_werkzeug=True)