import os
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import ClickEvent, ShortURL
from .schemas import URLCreate, URLCreated, URLStats
from .services import create_short_url

PUBLIC_BASE_URL = os.getenv(
    "PUBLIC_BASE_URL",
    "https://smart-url-shortener-ufi7.onrender.com"
).rstrip("/")

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Smart URL Shortener",
    description="Create short links, redirect visitors, and view basic click analytics.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

def to_created(record: ShortURL) -> URLCreated:
    return URLCreated(
        original_url=record.original_url,
        code=record.code,
        short_url=f"{PUBLIC_BASE_URL}/{record.code}",
        created_at=record.created_at,
    )

@app.get("/", tags=["health"])
def home():
    return {
        "message": "Smart URL Shortener is running",
        "docs": "/docs",
        "create_endpoint": "POST /api/urls",
    }

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

@app.post("/api/urls", response_model=URLCreated, status_code=status.HTTP_201_CREATED, tags=["URLs"])
def shorten_url(payload: URLCreate, db: Session = Depends(get_db)):
    try:
        record = create_short_url(db, str(payload.url), payload.custom_alias)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return to_created(record)

@app.get("/api/urls/{code}", response_model=URLStats, tags=["analytics"])
def get_url_stats(code: str, db: Session = Depends(get_db)):
    record = db.scalar(select(ShortURL).where(ShortURL.code == code))
    if not record:
        raise HTTPException(status_code=404, detail="Short URL not found")
    recent = db.scalars(
        select(ClickEvent.clicked_at)
        .where(ClickEvent.short_url_id == record.id)
        .order_by(ClickEvent.clicked_at.desc())
        .limit(20)
    ).all()
    return URLStats(
        original_url=record.original_url,
        code=record.code,
        short_url=f"{PUBLIC_BASE_URL}/{record.code}",
        created_at=record.created_at,
        click_count=record.click_count,
        recent_clicks=recent,
    )

@app.get("/{code}", include_in_schema=False)
def redirect_to_original(code: str, request: Request, db: Session = Depends(get_db)):
    record = db.scalar(select(ShortURL).where(ShortURL.code == code))
    if not record:
        raise HTTPException(status_code=404, detail="Short URL not found")

    record.click_count += 1
    db.add(ClickEvent(
        short_url_id=record.id,
        clicked_at=datetime.now(timezone.utc),
        user_agent=(request.headers.get("user-agent") or "")[:512] or None,
    ))
    db.commit()
    return RedirectResponse(url=record.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
