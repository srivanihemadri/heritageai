from pathlib import Path

path = Path("scripts/tasks_135_144_ai_voice_implementation.py")

source = path.read_text(encoding="utf-8")

old = """from app.models import register_models

register_models()

from app.api.v1.ai import router
"""

new = """from app.db.base import Base

# Import the application's model registry package so all ORM models
# are registered in Base.metadata.
import app.models  # noqa: F401

from app.api.v1.ai import router

if "scans" not in Base.metadata.tables:
    raise RuntimeError(
        "ORM model registry failed: scans table is not registered."
    )

print("ORM registration: PASS")
"""

if old not in source:
    raise RuntimeError(
        "Expected register_models() block was not found. "
        "No changes made."
    )

path.write_text(
    source.replace(old, new, 1),
    encoding="utf-8",
)

print("TASK 135-144 validation-script blocker repaired.")
print("Application source unchanged.")
print("register_models() dependency removed.")
print("ORM validation now uses existing Base.metadata architecture.")
