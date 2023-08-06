import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer


class IncomingTokenHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        token = self.path.split("=")[-1]
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><head><title>Success!</title></head>")
        self.wfile.write(b"<body><p>Authenticated!</p>")

        self.server.token = token
        time.sleep(1)
        self.wfile.write(b"<script>window.close()</script>")
        threading.Thread(target=self.server.shutdown, daemon=True).start()

    def log_message(self, format, *args):
        """Don't log incoming requests to stderr"""
        pass


def wait_for_token_reply() -> str:
    server_address = ("localhost", 8123)
    httpd = HTTPServer(server_address, IncomingTokenHandler)
    httpd.serve_forever()
    return httpd.token
