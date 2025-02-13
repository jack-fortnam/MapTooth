import asyncio,bluetooth,pickle,uuid,time

from websockets.asyncio.client import connect

server_ip = "192.168.1.93"
uri = f"ws://{server_ip}:8765"
print(f"{uuid.getnode()} is connecting to the server at {server_ip}")

async def report_out():
    try:
        async with connect(uri) as websocket:
            nearby_devices = bluetooth.discover_devices(lookup_names=True)
            report = [uuid.getnode()]
            for addr, name in nearby_devices:
                report.append([addr,name])
            data = pickle.dumps(report)
            print(f"Report: {report}")
            await websocket.send(data)
    except:
        print(f"{server_ip} not responding please check the server and try again")

if __name__ == "__main__":
    while True:
        asyncio.run(report_out())
        time.sleep(10)