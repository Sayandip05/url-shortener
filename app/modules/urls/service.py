import string
import random
from sqlalchemy.orm import Session
from app.modules.urls.models import URL
from app.core.config import settings

BASE62_CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase
SHORT_CODE_LENGTH = 7


def _generate_short_code() -> str:
    return "".join(random.choices(BASE62_CHARS, k=SHORT_CODE_LENGTH))


def get_or_create_short_url(db: Session, long_url: str) -> URL:
    existing = db.query(URL).filter(URL.long_url == long_url).first()
    if existing:
        return existing

    # Generate a unique code (retry on collision)
    for _ in range(5):
        code = _generate_short_code()
        if not db.query(URL).filter(URL.short_code == code).first():
            break
    else:
        raise RuntimeError("Failed to generate a unique short code")

    url_entry = URL(short_code=code, long_url=long_url)
    db.add(url_entry)
    db.commit()
    db.refresh(url_entry)
    return url_entry


def get_long_url(db: Session, short_code: str) -> URL | None:
    return db.query(URL).filter(URL.short_code == short_code).first()


def build_short_url(short_code: str) -> str:
    return f"{settings.base_url}/{short_code}"
