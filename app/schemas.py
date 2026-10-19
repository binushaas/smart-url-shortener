from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from typing import Optional

class URLCreate(BaseModel):
    url: HttpUrl
    custom_alias: Optional[str] = Field(default=None, min_length=3, max_length=16, pattern=r"^[A-Za-z0-9_-]+$")

class URLCreated(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    original_url: str
    code: str
    short_url: str
    created_at: datetime

class URLStats(BaseModel):
    original_url: str
    code: str
    short_url: str
    created_at: datetime
    click_count: int
    recent_clicks: list[datetime]
