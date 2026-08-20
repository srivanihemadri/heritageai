from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

BASE_DIR = Path(__file__).resolve().parents[2]
CA_CERT = BASE_DIR / "certs" / "ca.pem"

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": str(CA_CERT),
        }
    },
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
