# Smart URL Shortener with Analytics

A small backend service that creates short URLs, redirects visitors, and records basic click analytics. Built with FastAPI and SQLAlchemy.

## Features

- Create short links with automatically generated codes.
- Optional custom aliases.
- Redirect short links to their original destination.
- Count clicks and record click timestamps and user-agent strings.
- Retrieve analytics for a short link.
- Input validation and conflict/not-found errors.
- Interactive API documentation.
- Automated API tests.
- Docker support.

## Tech stack

- Python 3.12+
- FastAPI
- SQLAlchemy 2
- SQLite by default (can use a PostgreSQL URL via `DATABASE_URL`)
- pytest and HTTPX
- Docker

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API docs.

## API examples

### Create a short link

```bash
curl -X POST http://127.0.0.1:8000/api/urls \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com/some/long/path"}'
```

Optional custom alias:

```bash
curl -X POST http://127.0.0.1:8000/api/urls \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com","custom_alias":"example-link"}'
```

### Follow a short link

Open `http://127.0.0.1:8000/<code>` in a browser. Each successful redirect increments the click count.

### View analytics

```bash
curl http://127.0.0.1:8000/api/urls/<code>
```

The analytics response includes the original URL, code, creation time, total clicks, and the latest click timestamps.

## Tests

```bash
pytest -q
```

## Docker

```bash
docker build -t smart-url-shortener .
docker run --rm -p 8000:8000 -v url-data:/data smart-url-shortener
```

For a deployed service, set `PUBLIC_BASE_URL` to the public origin (for example, your deployed app's base URL). Set `DATABASE_URL` to a persistent database connection string when using a hosted database.

## Important notes

- This is a portfolio starter, not a production-hardened service.
- There is no user account system or link ownership model yet.
- The included analytics are basic; they do not attempt bot filtering or privacy-preserving aggregation.
- For public deployment, use a persistent database, HTTPS, rate limiting, abuse reporting, and monitoring. Do not claim these are implemented unless you add and test them.
- Keep secrets and real database credentials out of Git.
