import logging
import sys

import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from src.controllers.api_controllers import router

app = FastAPI(title="Système Distributeur PFE")


@app.middleware("http")
async def log_each_request(request: Request, call_next):
    """Trace chaque requête entrante (utile pour vérifier que le mobile atteint bien le PC)."""
    client_host = request.client.host if request.client else "?"
    print(f"[HTTP] {request.method} {request.url.path} client={client_host}", flush=True)
    return await call_next(request)


# Inclure toutes les routes définies dans le contrôleur
app.include_router(router, prefix="/api")


@app.on_event("startup")
def _configure_console_and_http_loggers():
    """Évite UnicodeEncodeError / 'charmap' sous Windows (logs HTTP, arabe, etc.)."""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    for name in (
        "urllib3",
        "urllib3.connectionpool",
        "urllib3.util.retry",
        "requests",
        "requests.packages.urllib3",
        "http.client",
    ):
        logging.getLogger(name).setLevel(logging.WARNING)


@app.on_event("startup")
def list_routes():
    print("\n--- ROUTES ENREGISTRÉES ---")
    for route in app.routes:
        print(f"[{route.methods}] {route.path}")
    print("---------------------------\n")

@app.get("/")
def home():
    return {"message": "Serveur opérationnel", "routes_prefix": "/api"}

@app.get("/test")
def test():
    return {"message": "Test OK"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)