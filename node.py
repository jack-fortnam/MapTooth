import asyncio,bluetooth,pickle,uuid,time,requests

from websockets.asyncio.client import connect

server_ip = "127.0.0.1"
uri = f"http://{server_ip}:80/report_in"
print(f"{uuid.getnode()} is connecting to the server at {uri}")

async def report_out():
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    report = [uuid.getnode()]
    for addr, name in nearby_devices:
        report.append([addr,name])
    data = pickle.dumps(report)
    print(f"Report: {report}")
    headers = {"Content-Type": "application/octet-stream"}
    response = requests.post(uri, data=data, headers=headers)

    print("Server response:", response.text)

if __name__ == "__main__":
    while True:
        asyncio.run(report_out())
        time.sleep(10)