import asyncio,bluetooth,pickle,uuid,time
from configparser import ConfigParser
from websockets.asyncio.client import connect

config = ConfigParser()
config.read('config.cfg')

server_ip = config.get('settings','server_ip')
port = config.get('settings','port')
uri = f"http://{server_ip}:{port}"
print(f"{uuid.getnode()} is connecting to the server at {uri}")

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
        print(f"{uri} not responding please check the server and try again")

if __name__ == "__main__":
    while True:
        asyncio.run(report_out())
        time.sleep(10)