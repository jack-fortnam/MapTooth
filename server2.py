from flask import Flask, request, jsonify, render_template
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

@app.route('/node', methods=['GET'])
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
        id = request.args.get('id')
        return jsonify(locations[id])
    except:
        return jsonify(locations)

@app.route('/get-node', methods=['GET'])
def get_node():
    try:
        id = request.args.get('id')
        return jsonify(nodes[id])
    except:
        return jsonify(nodes)

@app.route('/report_in',methods=['POST'])
def report_in():
    try:
        report = pickle.loads(requests.data)
        device_id = f"{report[0]}"
        detected_devices = report[1:]
        locations[device_id] = detected_devices

        print(f"Updated locations: {locations}")
        return "Data received",200
    
    except Exception as e:
        return f"Error: {str(e)}",400
    
#async def get_locations(request):
#    return web.json_response(locations)

# Main driver function
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)