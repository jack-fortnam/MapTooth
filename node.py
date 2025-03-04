import asyncio
import json
import uuid
import time
import requests
from bleak import BleakScanner

server_ip = "127.0.0.1"
uri = f"http://{server_ip}:5000/report_in"
print(f"{uuid.getnode()} is connecting to the server at {uri}")

async def scan_bluetooth():
    devices = await BleakScanner.discover()
    device_list = []
    for device in devices:
        device_list.append({"address": device.address, "name": device.name or "Unknown"})
    return device_list

async def report_out():
    report = {
        "device_id": uuid.getnode(),
        "nearby_devices": await scan_bluetooth()
    }
    data = json.dumps(report).encode("utf-8")
    print(f"Report: {json.dumps(report, indent=2)}")
    headers = {"Content-Type": "application/json"}
    response = requests.post(uri, data=data, headers=headers)
    print("Server response:", response.text)

if __name__ == "__main__":
    while True:
        asyncio.run(report_out())
        time.sleep(10)
