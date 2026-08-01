# gritiva-showcase

A tiny end-to-end deployment showcase on Gritiva: a stdlib-only Python web app
with a landing page and a JSON API. Zero third-party dependencies.

## Endpoints

| Path          | Description                               |
|---------------|-------------------------------------------|
| `/`           | Landing page (static HTML)                |
| `/api/health` | Liveness check -> `{"status": "ok", ...}` |
| `/api/stats`  | Uptime / Python / host info               |

## Run locally

```bash
python3 server.py            # listens on 0.0.0.0:8080
PORT=8090 python3 server.py  # custom port
```
