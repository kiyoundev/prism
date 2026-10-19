import os
from fastapi import FastAPI
from app.config import DATABASE_URL, ANTHROPIC_API_KEY, INTERNAL_API_KEY  # noqa: F401 — validates env vars at startup
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allowed origins: comma-separated list via env var in production (Railway),
# falls back to localhost for local dev.
# Example Railway env var: ALLOWED_ORIGINS=https://prism.vercel.app,https://prism-*.vercel.app
_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
allowed_origins = [o.strip() for o in _origins_env.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


# TODO: add API key middleware — validate X-API-Key header on all /v1/* routes
# against INTERNAL_API_KEY env var. Next.js proxy route sets this header.
# Use FastAPI dependencies or middleware; return 401 if missing or invalid.

# TODO: before calling Phase 3 (Claude), compute SHA-256 of normalized SMS text and
# check message_analysis for a recent result with the same hash. Return cached result
# if found to avoid redundant Claude API calls and control cost.
