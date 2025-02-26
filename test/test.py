from flask import Flask, request

import pickle

app = Flask(__name__)

@app.route('/send_pickle', methods=['POST'])
def receive_pickle():
    try:
        # Get and unpickle the data
        pickled_data = request.data
        received_object = pickle.loads(pickled_data)

        print("Received object:", received_object)

        return "Pickle received successfully", 200

    except Exception as e:
        return f"Error: {str(e)}", 400

if __name__ == '__main__':
    app.run(debug=True)


import requests
import pickle

# Data to send
data = {"message": "Hello, Flask!", "id": 123}

# Serialize with pickle
pickled_data = pickle.dumps(data)

# Send to the Flask API
url = "http://127.0.0.1:5000/send_pickle"
headers = {"Content-Type": "application/octet-stream"}
response = requests.post(url, data=pickled_data, headers=headers)

print("Server response:", response.text)
