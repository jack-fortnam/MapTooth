# Importing required functions 
from flask import Flask, request, render_template 
import what3words
# Flask constructor 
app = Flask(__name__) 
api_key = "VPB535HB"
w3w = what3words.Geocoder(api_key)

# Root endpoint 
@app.route('/', methods=['GET']) 
def index(): 
    ## Display the HTML form template 
    return render_template('index.html') 

@app.route('/node',methods=['GET'])
def node():
    return render_template('node.html')
# `read-form` endpoint 
@app.route('/submitted', methods=['POST']) 
def submitted(): 

    # Get the form data as Python ImmutableDict datatype 
    data = request.form 
    nodeId = data['nodeID']
    nodeName = data['nodeName']
    what3 = data["w3w"]
    with open('locations.txt','a') as f:
        f.write(f"\n{nodeId},{nodeName},{what3}")
    return render_template('node.html',submitted = f"Node Submitted :D	{nodeId}	{nodeName}	{what3}")
# Main Driver Function 
if __name__ == '__main__': 
    # Run the application on the local development server 
    app.run()
