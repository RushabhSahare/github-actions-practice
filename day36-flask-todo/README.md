# Flask Todo App (Dockerized)

A small Flask todo list application backed by PostgreSQL. Originally written
around 2018 by JohnnyFang (https://github.com/JohnnyFang/flask-todo-app),
Dockerized here as part of the 90 Days of DevOps programme, Day 36.

The app has a simple web UI at `/` for viewing and adding todos, plus a small
JSON API:

- `GET /todo` returns all todo items
- `POST /todo` creates a new todo (body: `{"text": "..."}`)
- `POST /todo/delete` deletes todos by id (body: `{"ids": [1, 2]}`)

## Docker Hub

https://hub.docker.com/r/rushabhs7/day36-flask-todo

## Running with Docker Compose

Clone this repo, then from the project root:

docker compose:



This pulls the app image from Docker Hub and starts a Postgres 15 container
alongside it. The app will be reachable at `http://<host>:8080`.

## Environment Variables

Set in a `.env` file in the project root:

| Variable            | Purpose                              |
|---------------------|---------------------------------------|
| POSTGRES_USER       | Database username                    |
| POSTGRES_PASSWORD   | Database password                    |
| POSTGRES_DB         | Database name                        |
| SECRET_KEY          | Flask secret key                     |

Example values used during development:


## Notes

Data persists in a named Docker volume, so `docker compose down` alone keeps
your todos. Use `docker compose down -v` to wipe the database completely.
