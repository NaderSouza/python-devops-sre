from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time, random

app = FastAPI(title="python-devops-sre")
REQS = Counter("http_requests_total", "Total HTTP requests", ["path", "method", "status"])
LAT = Histogram("http_request_duration_seconds", "Request duration", ["path", "method"])

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/work")
def work():
    t0 = time.time()
    # simula carga
    time.sleep(random.uniform(0.02, 0.2))
    LAT.labels("/work", "GET").observe(time.time() - t0)
    REQS.labels("/work", "GET", "200").inc()
    return {"result": "done"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


