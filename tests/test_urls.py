from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

TEST_DB_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)
client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_shorten_and_redirect():
    r = client.post("/api/v1/shorten", json={"long_url": "https://example.com"})
    assert r.status_code == 200
    data = r.json()
    assert "short_code" in data

    r2 = client.get(f"/{data['short_code']}", follow_redirects=False)
    assert r2.status_code == 302
    assert r2.headers["location"] in ("https://example.com", "https://example.com/")


def test_shorten_same_url_returns_same_code():
    r1 = client.post("/api/v1/shorten", json={"long_url": "https://dedup.example.com"})
    r2 = client.post("/api/v1/shorten", json={"long_url": "https://dedup.example.com"})
    assert r1.json()["short_code"] == r2.json()["short_code"]
