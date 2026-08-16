from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import app

print("TASK 10A — APPLICATION IMPORT")
print("FastAPI application:", type(app).__name__)

client = TestClient(app)

print("TestClient: PASS")

routes = []

for route in app.routes:
    path = getattr(route, "path", None)
    methods = getattr(route, "methods", None)

    if path and methods:
        routes.append((path, sorted(methods)))

print()
print("SCANNER ROUTES")

for path, methods in routes:
    if "/ai/scan" in path:
        print(path, methods)

print()
print("TASK 10A COMPLETE")
print("NO GEMINI REQUEST")
print("NO DATABASE CHANGES")
