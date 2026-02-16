#!/usr/bin/env python3
"""Simple HTTP server for the arxiv cards display."""
import http.server
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
port = 8080
print(f"Serving at http://localhost:{port}")
http.server.HTTPServer(("", port), http.server.SimpleHTTPRequestHandler).serve_forever()
