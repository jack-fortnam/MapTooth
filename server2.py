from flask import Flask, request, jsonify, render_template,redirect,make_response
import json
from configparser import ConfigParser
import ast,utils
import jwt
import datetime

# Flask setup
app = Flask(__name__)
app.url_map.strict_slashes = False
# Constants and storage
locations = {}
nodes = {}
config = ConfigParser()
config.read("config.cfg")
ip = config['CORE']['server_ip']
port = config['CORE']['port']
SECRET_KEY = config['CORE']['secret']

try:
    with open('nodes.json','r') as nodeo:
        nodes = json.load(nodeo)
except:
    nodes = []

def login_input_check(username, password):
    user_data = config.get("USERS", "root", fallback=None)
    
    if user_data:
        try:
            user_dict = ast.literal_eval(user_data)  # Safely parse the string as a dictionary
            correct_user = user_dict.get('user')
            correct_pass = user_dict.get('password')
            salt = user_dict.get('salt')

            password = utils.encrypt(password,salt)
        except (SyntaxError, ValueError):
            return False  # Return False if parsing fails
    if correct_user == username and correct_pass == password:
        return True
    return False

def create_jwt_token(username):
    expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
    payload = {"user": username, "exp": expiration}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def get_logged_in_user():
    token = request.cookies.get("auth_token")
    if not token:
        return None
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["user"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def secure(target_page):
    user = get_logged_in_user()
    if not user:
        return redirect("/login")  # Redirect if not logged in

    return render_template(target_page)

@app.route('/', methods=['GET'])
def index():
    try:
        with open("nodes.json", "r") as file:
            nodes = json.load(file)  # Load JSON data properly
    except json.JSONDecodeError:
        nodes = {}  # Handle empty or invalid JSON file

    print("Loaded nodes:", nodes)

    markers = []
    for location_id, (place_name, coords) in nodes.items():
        coords = coords.strip().split(',')
        lat,lng = coords[0],coords[1]
        print(locations)
        devices = locations.get(location_id)
        markers.append((lat, lng, place_name,location_id,devices))

    print("Final markers:", markers)
    return render_template("map.html", markers=markers)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin')
def admin():
    return secure('admin.html')

@app.route('/logg' , methods=['POST'])
def logg():
    data = request.form
    userID = data['userID']
    password = data['password']
    if login_input_check(userID,password):
        token = create_jwt_token(userID)
        resp = make_response(redirect("/admin"))
        resp.set_cookie("auth_token", token, httponly=True, secure=True, max_age=7*24*60*60)
        return resp
    return "Invalid credentials", 401

@app.route('/admin/node', methods=['GET'])
def node():
    return secure('node.html')

@app.route('/submitted', methods=['POST'])
def submitted():
    data = request.form
    nodeId = data['nodeID']
    nodeName = data['nodeName']
    coord = data['coord']
    nodes[nodeId] = [nodeName,coord]
    with open('nodes.json', 'w') as nodeo:
        json.dump(nodes,nodeo)
    return render_template('node.html', submitted=f"Node Submitted!<br> {nodeId}<br> {nodeName}<br> {coord}")

@app.route('/get-locations', methods=['GET'])
def get_locations():
    try:
        id = int(request.args.get('id'))
        return jsonify(locations[id])
    except:
        return jsonify(locations)
    
@app.route('/get-node', methods=['GET'])
def get_node():
    try:
        id = str(request.args.get('id'))
        print(id)
        print(nodes[id])
        return jsonify(nodes[id])
    except:
        return jsonify(nodes)

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

if __name__ == '__main__':
    app.run(host=ip or '0.0.0.0', port=port)
