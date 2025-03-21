import socket
from http.server import BaseHTTPRequestHandler, HTTPServer


def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))  # Connect to an external server (Google DNS)
        return s.getsockname()[0]


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/ping":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Pong")

        elif self.path == "/status":
            # status = game_logic.get_status()
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"result of get_status()")

        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self):
        if self.path == "/action":
            # game_logic.action()
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            print(f"Received move: {post_data}")
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Action received")

        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found"))


host = "0.0.0.0"  # Listen on all available network interfaces

port = 8000

def run_server():
    server = HTTPServer((host, port), ServerHandler)
    print(f"Serving on http://{get_local_ip()}:{port}")
    server.serve_forever()
