import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from config.logging_config import configure_logging
from src.api.v1.router import api_router
from src.core.config import get_settings
from src.core.database import init_db
from src.core.telemetry import REQUEST_COUNT, REQUEST_LATENCY, metrics_response
from src.mlops.langsmith_tracing import configure_langsmith

settings = get_settings()
configure_logging()
configure_langsmith()

@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield

app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)

@app.middleware("http")
async def observability(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    REQUEST_COUNT.labels(request.method, request.url.path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.url.path).observe(time.perf_counter() - started)
    return response

@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.app_name}

@app.get("/metrics", include_in_schema=False)
async def metrics():
    return metrics_response()
