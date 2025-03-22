import json
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import wraps

from sstpyg.server.main import GameEngine


HOST = "0.0.0.0"  # Listen on all available network interfaces
PORT = 8000


def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))  # Connect to an external server (Google DNS)
        return s.getsockname()[0]


def prepare_response(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            message = func(self, *args, **kwargs)
            self.send_response(200)
        except NotFoundError:
            message = "Not Found"
            self.send_response(404)

        except Exception:
            message = "Internal Server Error"
            self.send_response(500)

        if isinstance(message, (dict, list)):
            message = json.dumps(message)
            self.send_header("Content-type", "application/json")
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(message.encode())
    return wrapper


class NotFoundError(Exception):
    pass


class ServerHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.game_engine = GameEngine()
        super().__init__(*args, **kwargs)

    @prepare_response
    def do_GET(self):
        if self.path.startswith("/initialize/"):
            role = self.path.split("/initialize/")[-1]
            response = self.game_engine.initialize(role)
            return response

        elif self.path == "/status":
            return self.game_engine.get_status()

        else:
            raise NotFoundError()

    @prepare_response
    def do_POST(self):
        if self.path == "/command":
            content_length = int(self.headers.get("Content-Length", 0))
            command_body = json.loads(self.rfile.read(content_length))
            return  self.game_engine.command(command_body)

        else:
            raise NotFoundError()


def run_server():
    server = HTTPServer((HOST, PORT), ServerHandler)
    print(f"Serving on http://{get_local_ip()}:{PORT}")
    server.serve_forever()
