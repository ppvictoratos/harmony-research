from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes

# Schema is managed by Alembic (alembic upgrade head), not create_all
app = FastAPI(title="Harmony Research API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)


@app.get("/health")
def health():
    return {"status": "ok"}
