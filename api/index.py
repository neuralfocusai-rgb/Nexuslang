from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def get(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())
