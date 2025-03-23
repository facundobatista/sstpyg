import json
import socket

from aiohttp import web

from sstpyg.server.main import Engine

engine = Engine()
engine.init()


def jsonify(obj):
    text = json.dumps(obj)
    return web.Response(text=text, content_type="application/json")


async def initialize(request):
    role = request.match_info.get("role")
    await engine.add_client(role)
    return web.Response(text="")


async def status(request):
    state = await engine.get_state()
    return jsonify(state)


async def command(request):
    data = await request.json()
    result = await engine.command(data)
    return jsonify(result)


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

    async def init_engine(app):
        await engine.init()

    app.on_startup.append(init_engine)
    web.run_app(app)
