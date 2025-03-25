import asyncio
from configparser import ConfigParser
import json
import uuid
import time
import requests
from bleak import BleakScanner

try:
    config = ConfigParser()
    config.read("config.cfg")
    port = config['CORE']['port']
    server_ip = config['CORE']['server_ip']
    uri = f"http://{server_ip}:{port}/report_in"
except:
    print("No config generated. use setup.py to configure")
    exit()
print(f"{uuid.getnode()} is connecting to the server at {uri}")

async def scan_bluetooth():
    try:
        devices = await BleakScanner.discover()
    except:
        print("Bluetooth is not on")
        exit()
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
