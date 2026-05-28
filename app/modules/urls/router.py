from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.urls import service
from app.modules.urls.schemas import ShortenRequest, ShortenResponse

router = APIRouter(tags=["urls"])
redirect_router = APIRouter(tags=["redirects"])


@router.post("/shorten", response_model=ShortenResponse)
def shorten_url(payload: ShortenRequest, db: Session = Depends(get_db)):
    long_url = str(payload.long_url)
    url_entry = service.get_or_create_short_url(db, long_url)
    return ShortenResponse(
        short_url=service.build_short_url(url_entry.short_code),
        long_url=url_entry.long_url,
        short_code=url_entry.short_code,
        created_at=url_entry.created_at,
    )


@redirect_router.get("/{short_code}", include_in_schema=False)
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    url_entry = service.get_long_url(db, short_code)
    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(url=url_entry.long_url, status_code=302)
