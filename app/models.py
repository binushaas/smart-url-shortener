from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base
from typing import Optional

def utcnow():
    return datetime.now(timezone.utc)

class ShortURL(Base):
    __tablename__ = "short_urls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    original_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    code: Mapped[str] = mapped_column(String(16), unique=True, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    click_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    clicks: Mapped[list["ClickEvent"]] = relationship(back_populates="short_url", cascade="all, delete-orphan")

class ClickEvent(Base):
    __tablename__ = "click_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    short_url_id: Mapped[int] = mapped_column(ForeignKey("short_urls.id"), index=True, nullable=False)
    clicked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    user_agent: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    short_url: Mapped[ShortURL] = relationship(back_populates="clicks")
