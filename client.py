import requests
r = requests.get('http://localhost:8080/locations')
print(r.json()) # if response type was set to JSON, then you'll auto