from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# Local development uses certs/ca.pem.
# Render provides the certificate as /etc/secrets/ca.pem.
render_ca = Path("/etc/secrets/ca.pem")
local_ca = Path(__file__).resolve().parents[2] / "certs" / "ca.pem"

if render_ca.exists():
    ca_path = render_ca
elif local_ca.exists():
    ca_path = local_ca
else:
    raise FileNotFoundError(
        "Aiven CA certificate not found. "
        "Expected /etc/secrets/ca.pem on Render or certs/ca.pem locally."
    )

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": str(ca_path),
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
