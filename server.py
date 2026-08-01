#!/usr/bin/env python3
"""gritiva-showcase — a tiny stdlib-only web app.

Endpoints:
  GET /            -> pretty HTML landing page
  GET /api/health  -> JSON health status
  GET /api/stats   -> JSON runtime stats

No external dependencies: only the Python standard library.
"""
import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

START_TIME = time.time()
REQUESTS = 0
PORT = int(os.environ.get("PORT", "8080"))


class Handler(BaseHTTPRequestHandler):
    server_version = "gritiva-showcase/1.0"

    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj, indent=2, ensure_ascii=False), "application/json")

    def do_GET(self):
        global REQUESTS
        REQUESTS += 1
        path = urlparse(self.path).path
        if path == "/":
            self._serve_index()
        elif path == "/api/health":
            self._json({
                "status": "ok",
                "service": "gritiva-showcase",
                "uptime_seconds": round(time.time() - START_TIME, 1),
            })
        elif path == "/api/stats":
            self._json(self._stats())
        else:
            self._json({"error": "not found", "path": path}, 404)

    def _serve_index(self):
        here = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(here, "index.html"), "rb") as f:
            self._send(200, f.read())

    def _stats(self):
        return {
            "service": "gritiva-showcase",
            "version": "1.0.0",
            "python": sys.version.split()[0],
            "pid": os.getpid(),
            "uptime_seconds": round(time.time() - START_TIME, 1),
            "total_requests": REQUESTS,
        }

    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), fmt % args))


if __name__ == "__main__":
    srv = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"gritiva-showcase listening on 0.0.0.0:{PORT}")
    srv.serve_forever()
