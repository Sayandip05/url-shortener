from pydantic import BaseModel, HttpUrl, ConfigDict
from datetime import datetime


class ShortenRequest(BaseModel):
    long_url: HttpUrl


class ShortenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    short_url: str
    long_url: str
    short_code: str
    created_at: datetime
