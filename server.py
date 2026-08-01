#!/usr/bin/env python3
"""gritiva-showcase - a tiny stdlib-only web app.

Serves a static landing page (/) and a small JSON API:
    GET /api/health -> {"status": "ok"}
    GET /api/stats  -> uptime / python / host info

No third-party dependencies. Python 3 only.
"""
import json
import os
import platform
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

STARTED_AT = time.time()
HERE = Path(__file__).resolve().parent
PORT = int(os.environ.get("PORT", "8080"))

INDEX_HTML = HERE / "index.html"


def stats():
    return {
        "app": "gritiva-showcase",
        "version": "1.0.0",
        "uptime_seconds": round(time.time() - STARTED_AT, 2),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "hostname": platform.node(),
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "GritivaShowcase/1.0"

    def _reply(self, code, payload, content_type="application/json"):
        body = payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/api/health":
            self._reply(200, {"status": "ok", "service": "gritiva-showcase"})
        elif path == "/api/stats":
            self._reply(200, stats())
        elif path in ("/", "/index.html"):
            if INDEX_HTML.exists():
                self._reply(200, INDEX_HTML.read_bytes(), "text/html; charset=utf-8")
            else:
                self._reply(500, {"error": "index.html missing"})
        else:
            self._reply(404, {"error": "not found", "path": path})

    def log_message(self, fmt, *args):
        print("[%s] %s" % (self.log_date_time_string(), fmt % args))


if __name__ == "__main__":
    print("gritiva-showcase starting on 0.0.0.0:%d" % PORT, flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
