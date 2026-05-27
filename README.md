# URL Shortener — FastAPI Boilerplate

A minimal URL shortener built with FastAPI, following a **modular monolith** architecture.

## Project Structure

```
url-shortener/
├── app/
│   ├── main.py               # App entrypoint, router registration
│   ├── core/
│   │   ├── config.py         # Settings (pydantic-settings + .env)
│   │   └── database.py       # SQLAlchemy engine, session, Base
│   └── modules/
│       ├── urls/             # URL shortening module
│       │   ├── models.py     # SQLAlchemy ORM model
│       │   ├── schemas.py    # Pydantic request/response schemas
│       │   ├── service.py    # Business logic
│       │   └── router.py     # FastAPI routes
│       └── health/
│           └── router.py     # Health check endpoint
├── tests/
│   └── test_urls.py
├── run.py                    # Creates DB tables + starts uvicorn
└── requirements.txt
```

Each module owns its own models, schemas, service, and router. Adding a new feature = adding a new folder under `modules/`.

## Quickstart

```bash
pip install -r requirements.txt
python run.py
```

API docs available at `http://localhost:8000/docs`.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/shorten` | Shorten a long URL |
| GET | `/{short_code}` | Redirect to original URL |
| GET | `/health` | Health check |

### Shorten a URL

```bash
curl -X POST http://localhost:8000/api/v1/shorten \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://example.com/some/very/long/path"}'
```

```json
{
  "short_url": "http://localhost:8000/abc1234",
  "long_url": "https://example.com/some/very/long/path",
  "short_code": "abc1234",
  "created_at": "2024-01-01T00:00:00"
}
```

## Configuration (`.env`)

```
BASE_URL=https://yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost/urldb
```

## Run Tests

```bash
pytest tests/
```
