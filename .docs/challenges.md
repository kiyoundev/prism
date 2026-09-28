# Prism — Challenges & Clarifications

A running log of architectural questions, confusions, and the reasoning behind decisions.

---

## Why does Vercel/Railway change the Docker strategy?

**Question:** In a previous project, everything ran in Docker (frontend, backend, databases) and the same containers deployed to production. Why is Prism different?

**Answer:**

The core value of Docker is environment parity — your local container is byte-for-byte identical to what runs in production. That holds when you control the production runtime (e.g. ECS, VPS, Fly.io): you build an image, ship it, and it runs the same way everywhere.

Vercel and Railway break that assumption because **you don't ship a Docker image — you ship code and they build it themselves.**

- **Vercel** takes `frontend/`, runs `npm run build` on their infrastructure, and serves it. Their build environment is a black box. Dockerizing Next.js locally doesn't give you parity with Vercel — it just adds a layer. Running `next dev` locally and letting Vercel run `next build` is close enough.

- **Railway** detects Python, installs from `requirements.txt`, and runs `uvicorn`. You can influence it (Prism uses `runtime.txt` to pin Python 3.12), but Railway still manages the container — you're not shipping your own image.

So the parity argument weakens for both services. The one gap that *does* matter is the **database**: a local Postgres container (via docker-compose) behaves like Supabase much better than SQLite or mocks. That's what Issue #9's docker-compose targets — not full environment parity, just a real Postgres for local dev.

**Summary:**
- Previous project: Docker = dev tool + deployment unit (full parity)
- Prism: Docker = dev tool only for local Postgres; Vercel/Railway handle their own runtimes

---

## Why does the Next.js proxy need both FASTAPI_URL and INTERNAL_API_KEY?

**Question:** Why not just call FastAPI directly from the browser? Why the two separate env vars?

**Answer:**

Railway gives FastAPI a public URL — anyone on the internet can reach it. Without protection, anyone who finds that URL could spam `/v1/score`, rack up Anthropic API costs, or scrape the database.

The proxy pattern solves this:

```
Browser → Next.js (Vercel) → FastAPI (Railway)
           ↑ public           ↑ "private"
```

- **`FASTAPI_URL`** — tells Next.js where FastAPI lives. Kept server-side so the Railway URL never reaches the browser.
- **`INTERNAL_API_KEY`** — a shared secret Next.js attaches as an `X-API-Key` header on every request to FastAPI. FastAPI rejects requests without it. Even if someone finds the Railway URL, they can't use it without the key.

`FASTAPI_URL` is the address. `INTERNAL_API_KEY` is the lock on the door.

---

## Why is CORS less important given the proxy pattern?

**Question:** The backend has `ALLOWED_ORIGINS`. Why does it matter if the browser never calls FastAPI directly?

**Answer:**

It largely doesn't — for Prism's architecture. CORS is a browser security rule that only applies to browser-initiated requests. Since Next.js proxies all calls server-to-server, the browser never makes a cross-origin request to Railway and CORS is bypassed entirely.

`ALLOWED_ORIGINS` on the backend is a safety net for:
- Direct API testing via Swagger UI (`/docs`)
- Any future case where the browser calls FastAPI directly

For MVP it could be left as a placeholder without breaking anything. It's set as a best practice.

---

## Which env vars live where, and why?

**Question:** There are env vars on Railway, on Vercel, and in local `.env` files. What's the difference and where does each one go?

**Answer:**

Each service only gets the vars it needs:

**Railway (backend):**
- `DATABASE_URL` — Supabase connection string. FastAPI needs this to talk to Postgres.
- `ANTHROPIC_API_KEY` — Claude API key. Used by Phase 3.
- `INTERNAL_API_KEY` — shared secret. FastAPI checks incoming requests for this.
- `ALLOWED_ORIGINS` — which frontend URLs are allowed for CORS.

**Vercel (frontend):**
- `FASTAPI_URL` — the Railway backend URL. Next.js proxy reads this server-side to know where to forward requests.
- `INTERNAL_API_KEY` — same shared secret as Railway. Next.js attaches it as `X-API-Key` on every proxied request.

**Local dev (`frontend/.env.local`, `backend/.env`):**
- Same vars as above but pointing at local services (`FASTAPI_URL=http://localhost:8000`, local Postgres, etc.).
- These files are gitignored — never committed.

**`.env.example` files (committed):**
- Placeholder versions of the above. Document what vars are needed so any developer cloning the repo knows what to fill in.

The `INTERNAL_API_KEY` is the one var that must match exactly on both sides (Railway and Vercel) — it's the shared password the frontend uses to prove it's the legitimate caller to the backend.

---

## How env var validation works in frontend and backend

**Question:** How do env vars get validated at startup, and what's the pattern?

**Answer:**

The pattern is the same in both languages: **validate at import time, export typed constants, one file owns all env vars.**

### Frontend — `src/lib/env.ts`

```typescript
import "server-only";

function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) throw new Error(`Missing required environment variable: ${name}`);
  return value;
}

export const env = {
  FASTAPI_URL: requireEnv("FASTAPI_URL"),
  INTERNAL_API_KEY: requireEnv("INTERNAL_API_KEY"),
};
```

Three things working together:

1. **`import "server-only"`** — Next.js will throw a build error if this file is ever imported in a Client Component. Hard compile-time guarantee that secrets never reach the browser. Without this, you could accidentally import `env` in a `"use client"` file and Next.js would silently expose the vars.

2. **`requireEnv` runs at module load time** — the `export const env = { ... }` block executes when the file is first imported. So the first time any server-side code imports `env`, validation runs immediately. You get a clear error at startup, not a cryptic `undefined` somewhere deep in a fetch call.

3. **Single source of truth** — every server-side file that needs these vars imports from `env.ts`. If you add a new required var, you add it in one place.

### Backend — `app/config.py`

```python
import os, sys

def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        sys.exit(f"Missing required environment variable: {name}")
    return value

DATABASE_URL = require_env("DATABASE_URL")
ANTHROPIC_API_KEY = require_env("ANTHROPIC_API_KEY")
INTERNAL_API_KEY = require_env("INTERNAL_API_KEY")
```

Same idea — module-level constants means `require_env` runs the moment Python imports `config.py`. `main.py` imports from `config.py`, so FastAPI fails before it ever binds to a port.

`sys.exit()` instead of raising an exception because a missing env var at startup is not a recoverable error — you want a clean exit with a readable message in the Railway logs, not a traceback.

---

## Python version alignment — local vs. Railway

**Question:** Does the local Python version need to match Railway?

**Answer:**

Yes — `runtime.txt` pins Railway to Python 3.12. Local dev should match.

The risk of mismatching isn't that things break immediately — it's subtle issues that are hard to diagnose:
- A package in `requirements.txt` might behave differently on 3.9 vs 3.12
- Some syntax works on 3.12 but not 3.9 (e.g. `type` aliases, `match` statements)
- You'd be testing against a different runtime than what ships

**Required versions:**
- Python: **3.12** (matches `backend/runtime.txt`)
- Node.js: whatever Vercel uses (Next.js handles this — just keep `package.json` deps current)

**Setup:** Create a virtual environment using Python 3.12 inside `backend/`:
```bash
python3.12 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt
pip install ruff  # dev tooling
```

Activate the venv whenever working on backend code. Issue #9 (docker-compose) will formalize this further.

---

## Local dev workflow vs. Railway

**Question:** If I implement a new feature and want to test it locally, Railway wouldn't reflect that change.

**Answer:** Correct — Railway is production/staging, not a dev sandbox. Local dev runs FastAPI directly:

```
Terminal 1: cd backend && uvicorn app.main:app --reload
Terminal 2: cd frontend && npm run dev
```

`frontend/.env.local` points `FASTAPI_URL` at `localhost:8000`. You develop and test the full stack locally, then push to the remote repo when confident. Railway picks up the push automatically and deploys.

Issue #9 (docker-compose) formalizes this: `docker-compose up` replaces the two terminals and adds a local Postgres so you're not dependent on Supabase for every dev session.

---

## When to use docker-compose vs. running services natively

**Question:** Should docker-compose auto-launch when working on Prism? Does `npm run dev` boot Docker?

**Answer:**

No — docker-compose is intentional, not automatic. `npm run dev` at the root starts Next.js and uvicorn natively without Docker.

The reason: `docker compose up` builds the image on first run (takes a minute) and keeps Postgres + FastAPI running in the background. You don't always need that — working on frontend only doesn't require a database.

**Three workflows depending on what you're working on:**

| Scenario | Command |
|---|---|
| Frontend only | `npm run dev:frontend` |
| Backend only (no DB needed) | `npm run dev:backend` |
| Full stack with database | `docker compose up` + `npm run dev:frontend` |

Auto-launching Docker on system startup would waste memory and CPU when you're not working on Prism. Keep it manual.
