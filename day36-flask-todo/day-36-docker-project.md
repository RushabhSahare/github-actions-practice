# Day 36: Docker Project, Dockerize a Real Application

## App Chosen

JohnnyFang/flask-todo-app, a small Flask app with a Postgres backend and a
simple web UI plus JSON API for managing a todo list. I picked it because it
was genuinely undockerized (no Dockerfile, no compose file anywhere in the
repo) and small enough to stay comfortable on a t3.micro with 908 MiB RAM
and no swap, which has caused OOM issues on previous days.

## Dockerfile

```dockerfile
# Build stage: compile dependencies into a venv
FROM python:3.8-slim AS builder

WORKDIR /app

# gcc and libpq-dev are only needed here to build any psycopg2-binary
# wheels that don't have a matching prebuilt version; not needed in the
# final image, which is why this whole stage gets discarded later
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Final stage: clean slim image, no build tools, no apt cache
FROM python:3.8-slim

RUN useradd --create-home appuser
WORKDIR /app

# Bring in only the installed venv from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

# Run as a non root user rather than the container default of root
USER appuser

EXPOSE 5000

CMD ["python", "run.py"]
```

Python 3.8 was chosen deliberately, not as the latest version, because the
app's dependencies (Flask 1.0.2, Flask-SQLAlchemy 2.3.2, marshmallow 2.x)
are from 2018 and break under newer Python and newer transitive
dependencies, as described below.

## Challenges Faced

**1. Missing instance config.** The app calls
`app.config.from_pyfile('config.py')` expecting a file at `instance/config.py`
that simply did not exist in the repo. Had to create it myself with the
database URL and secret key, sourced from environment variables so Compose
can inject them.

**2. SQLAlchemy version conflict.** First build failed with: AttributeError: module 'sqlalchemy' has no attribute 'all'



`flask_sqlalchemy==2.3.2` was pinned in requirements.txt but plain
`SQLAlchemy` was not, so pip grabbed the latest SQLAlchemy 2.x. Flask
SQLAlchemy 2.3.2 reaches into internals that no longer exist in SQLAlchemy
2.x. Fixed by explicitly pinning `SQLAlchemy==1.2.19`, matching the era of
the other pinned packages.

**3. psycopg2 build dependency.** The original requirements.txt used
`psycopg2` rather than `psycopg2-binary`, which needs a C compiler and
`libpq-dev` present at install time. Switched to `psycopg2-binary` so the
final image doesn't need to carry build tools at all, keeping it smaller.

**4. A typo, not a real bug.** While hand editing `instance/config.py`, a
stray keystroke turned `False` into `Falsewq`, which crashed the app with a
`NameError` on startup. A good reminder that not every crash is a
dependency problem, sometimes it's just a fat fingered edit.

**5. Docker Hub tag mistake.** First push attempt used a literal placeholder
username instead of my real Docker Hub username, resulting in
`push access denied`. Retagging with the correct username
(`rushabhs7/day36-flask-todo`) fixed it immediately.

**6. Compose still building locally instead of pulling.** During the fresh
pull test (Task 5), `docker images` showed `day36-flask-todo-app:latest`
rather than the Docker Hub image name, meaning Compose was still building
from the Dockerfile instead of pulling. The `docker-compose.yml` still had
`build: .` under the app service even after I thought I'd changed it to
`image: rushabhs7/day36-flask-todo:latest`. Rewriting the whole file
confirmed the fix, and the next `docker compose up` correctly showed
`Image rushabhs7/day36-flask-todo:latest Pulled`.

## Final Image Size

243 MB total disk usage, 59 MB unique content (the rest is shared base
layers like `python:3.8-slim` already present on the host).

## Docker Hub Link

https://hub.docker.com/r/rushabhs7/day36-flask-todo

## Verification

Ran the full fresh pull test: removed every local container and image,
then `docker compose up` with only the compose file present. Postgres and
the app both pulled from their registries, came up healthy, and a
`GET /todo` returned an empty list, confirming a genuinely clean start with
no leftover local state.
