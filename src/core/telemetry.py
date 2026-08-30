from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

REQUEST_COUNT = Counter("emakip_http_requests_total", "HTTP requests", ["method", "path", "status"])
REQUEST_LATENCY = Histogram("emakip_http_request_seconds", "HTTP request latency", ["path"])
AGENT_RUNS = Counter("emakip_agent_runs_total", "Agent workflow runs", ["route"])
RAG_QUERIES = Counter("emakip_rag_queries_total", "RAG retrieval queries")

def metrics_response() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
