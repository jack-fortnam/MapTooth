import asyncio,pickle,socket
from aiohttp import web
from websockets.asyncio.server import serve

locations = {}
IP = socket.gethostbyname(socket.gethostname())

async def report_in(websocket):
    data = await websocket.recv()
    report = pickle.loads(data)
    device_id = f"{report[0]}"
    detected_devices = report[1:]
    locations[device_id] = detected_devices

    print(f"Updated locations: {locations}")

async def get_locations(request):
    return web.json_response(locations)

async def start_http_server():
    app = web.Application()
    app.router.add_get("/locations", get_locations)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

async def main():
    asyncio.create_task(start_http_server())  # Start HTTP server
    async with serve(report_in, "0.0.0.0", 8765):
        await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    print(f"Server online at {IP}:8765 and data can be fetched at {IP}:8080") 
    asyncio.run(main())
    
