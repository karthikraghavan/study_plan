#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os

class LogHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/save-logs':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            logs = json.loads(body)
            
            # Save to same folder as this script
            with open('vk_logs.json', 'w') as f:
                json.dump(logs, f, indent=2)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'{"status":"saved"}')
        else:
            self.send_response(404)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
    
    def do_GET(self):
        if self.path == '/load-logs':
            try:
                with open('vk_logs.json', 'r') as f:
                    logs = json.load(f)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(logs).encode())
            except FileNotFoundError:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'[]')
        else:
            super().do_GET()
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.end_headers()

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print('Starting server on http://localhost:8000')
    print('Open: http://localhost:8000/index.html')
    HTTPServer(('localhost', 8000), LogHandler).serve_forever()
