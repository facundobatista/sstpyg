import json
import socket

from aiohttp import web

from sstpyg.server.main import Engine

engine = Engine()


def jsonify(obj):
    text = json.dumps(obj)
    return web.Response(text=text, content_type="application/json")


async def initialize(request):
    print("===== serving init")
    role = request.match_info.get("role")
    await engine.add_client(role)
    return web.Response(text="")


async def status(request):
    print("===== serving status?")
    state = await engine.get_state()
    print("===== serving status!", state)
    return jsonify(state)


async def command(request):
    print("===== serving command")
    data = await request.json()
    result = await engine.command(data)
    return jsonify(result)

#            content_length = int(self.headers.get("Content-Length", 0))
#            command_body = json.loads(self.rfile.read(content_length))
#            return  self.game_engine.command(command_body)


app = web.Application()
app.add_routes([
    web.get("/initialize/{role}", initialize),
    web.get("/status", status),
    web.post("/command", command),
])


def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        print("======== Local IP:", ip)

    web.run_app(app)
