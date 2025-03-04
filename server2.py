from flask import Flask, request, jsonify, render_template,redirect,make_response
import pickle,requests,json,hashlib
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
config.read("config.cfg")

try:
    with open('nodes.json','r') as nodeo:
        nodes = json.load(nodeo)
except:
    with open('nodes.json','w') as nodeo:
        pass

def login_input_check(username, password):
    correct_user = config.get("USERS", "root_user", fallback=None)
    correct_pass = config.get("USERS", "root_pass", fallback=None)
    
    if correct_user == username and correct_pass == password:
        return True
    return False


# Routes for HTML templates
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin')
def admin():
    return "Admin"

@app.route('/logg' , methods=['POST'])
def logg():
    data = request.form
    userID = data['userID']
    password = data['password']
    m = hashlib.sha256()
    m.update(password.encode())
    password = m.hexdigest()
    print(password)
    if login_input_check(userID,password):
        resp = redirect("/admin")
        resp.set_cookie('user',userID)
        resp.set_cookie('pass',password)
        return resp
    return "Invalid credentials", 401


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
        return jsonify(locations[id])
    except:
        return jsonify(locations)

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