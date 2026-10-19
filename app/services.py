import secrets
import string
from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import ShortURL
from typing import Optional

ALPHABET = string.ascii_letters + string.digits

def generate_code(length: int = 7) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))

def create_short_url(db: Session, original_url: str, custom_alias: Optional[str] = None) -> ShortURL:
    if custom_alias:
        existing = db.scalar(select(ShortURL).where(ShortURL.code == custom_alias))
        if existing:
            raise ValueError("That custom alias is already in use.")
        code = custom_alias
    else:
        code = generate_code()
        while db.scalar(select(ShortURL.id).where(ShortURL.code == code)) is not None:
            code = generate_code()

    record = ShortURL(original_url=str(original_url), code=code)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
