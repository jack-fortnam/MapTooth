from flask import Flask, request, jsonify, render_template,redirect,make_response
import pickle,requests,json
from configparser import ConfigParser
import asyncio,pickle,socket

# Flask setup
app = Flask(__name__)

# Constants and storage
api_key = "VPB535HB"
locations = {}
nodes = {}
IP = socket.gethostbyname(socket.gethostname())
config = ConfigParser()

try:
    with open('nodes.json','r') as nodeo:
        nodes = json.load(nodeo)
except:
    with open('nodes.json','w') as nodeo:
        pass

# Routes for HTML templates
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/admin/login')
def login():
    return render_template('login.html')

@app.route('/logg' , methods=['POST'])
def logg():
    data = request.form
    userID = data['userID']
    password = data['password']
    users = config['USERS']['root']
    return users

@app.route('/admin/node', methods=['GET'])
def node():
    return render_template('node.html')

@app.route('/submitted', methods=['POST'])
def submitted():
    data = request.form
    nodeId = data['nodeID']
    nodeName = data['nodeName']
    what3 = data['w3w']
    nodes[nodeId] = [nodeName,what3]
    with open('nodes.json', 'w') as nodeo:
        json.dump(nodes,nodeo)
    return render_template('node.html', submitted=f"Node Submitted :D {nodeId} {nodeName} {what3}")

@app.route('/get-locations', methods=['GET'])
def get_locations():
    try:
        id = int(request.args.get('id'))
        print(id)
        return jsonify(locations[id])
    except:
        return jsonify(locations)

"""@app.route('/get-node', methods=['GET'])
def get_node():
    try:
        id = request.args.get('id')
        print(id)
        print("Nodes dictionary:", json.dumps(nodes, indent=2))
        return jsonify(nodes[id])
    except:
        return jsonify(nodes)"""

@app.route('/report_in', methods=['POST'])
def report_in():
    try:
        report = request.get_json()  # Correctly parse JSON data
        if not report or "device_id" not in report or "nearby_devices" not in report:
            return "Invalid data format", 400
        
        device_id = report["device_id"]
        detected_devices = report["nearby_devices"]
        
        locations[device_id] = detected_devices  # Store data in locations dictionary

        print(f"Updated locations: {json.dumps(locations, indent=2)}")
        return "Data received", 200
    
    except Exception as e:
        return f"Error: {str(e)}", 400

    
#async def get_locations(request):
#    return web.json_response(locations)

# Main driver function
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)