from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes, studies
from app.config import settings

# Schema is managed by Alembic (alembic upgrade head), not create_all
app = FastAPI(title="Harmony Research API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)

app.include_router(routes.router)
app.include_router(studies.router)


@app.get("/health")
def health():
    return {"status": "ok"}
