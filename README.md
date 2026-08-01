# gritiva-showcase

A tiny, real web app deployed end-to-end on Gritiva.

## What it is

- **Landing page** — pretty HTML served at `/`
- **API** — two JSON endpoints using only the Python standard library:
  - `GET /api/health` → service status + uptime
  - `GET /api/stats` → runtime stats (python version, pid, request count)

## Run it locally

```bash
python3 server.py          # listens on 0.0.0.0:8080
PORT=9090 python3 server.py  # custom port
```

No dependencies. No `pip install`. Just Python 3.

## Deployed on Gritiva

Created from scratch: repo → scope on VM → automated pipeline deploy → port exposed to the internet.
