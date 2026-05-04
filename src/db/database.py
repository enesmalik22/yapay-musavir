"""
Veritabani baglanti yoneticisi.

SQLAlchemy engine ve session yonetimini saglar.
"""

import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.db.models import Base


# Proje kok dizini (yapay-musavir/)
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Veritabani dosyasi yolu
DB_PATH = PROJECT_ROOT / "data" / "yapay_musavir.db"

# SQLite baglanti URL'si
DATABASE_URL = f"sqlite:///{DB_PATH}"


# Engine: SQLAlchemy'nin DB ile konusan ana motor
engine = create_engine(
    DATABASE_URL,
    echo=False,  # True yaparsan SQL sorgularini terminalde gosterir (debug icin)
    connect_args={"check_same_thread": False}  # SQLite icin gerekli
)


# Session factory: her istekte yeni bir session olusturur
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Session:
    """
    Yeni bir veritabani session'i acar ve dondurur.
    Kullanim sonrasi mutlaka session.close() cagrilmalidir.
    
    Onerilen kullanim:
        db = get_db()
        try:
            # islemler...
            db.commit()
        finally:
            db.close()
    """
    return SessionLocal()


def init_db() -> None:
    """
    Veritabanini ve tum tablolari olusturur.
    Eger tablolar zaten varsa, dokunmaz.
    """
    # data/ klasoru yoksa olustur
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Tum modelleri DB'ye yaz
    Base.metadata.create_all(bind=engine)
    print(f"✅ Veritabani hazir: {DB_PATH}")


def reset_db() -> None:
    """
    DIKKAT: Tum tablolari siler ve yeniden olusturur.
    Tum veriler kaybolur!
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print(f"⚠️  Veritabani sifirlandi: {DB_PATH}")
