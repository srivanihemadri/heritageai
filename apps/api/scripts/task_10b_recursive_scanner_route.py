from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.routing import APIRoute
from app.main import app


print("=" * 80)
print("STEP 8C-003 — TASK 10B — RECURSIVE SCANNER ROUTE DISCOVERY")
print("=" * 80)


def inspect_routes(routes, prefix=""):
    for route in routes:

        path = getattr(route, "path", None)

        if path is None:
            path = ""

        full_path = prefix + path

        if isinstance(route, APIRoute):

            methods = sorted(route.methods or [])

            print(
                "APIRoute:",
                full_path,
                methods,
                "NAME=",
                route.name,
            )

            if (
                full_path == "/api/v1/ai/scan"
                and "POST" in methods
            ):
                print()
                print(">>> TARGET SCANNER ROUTE FOUND <<<")
                print("Path:", full_path)
                print("Methods:", methods)
                print("Endpoint:", route.endpoint)

                dependencies = []

                for dependency in route.dependant.dependencies:
                    call = getattr(
                        dependency.call,
                        "__name__",
                        str(dependency.call),
                    )

                    dependencies.append(call)

                print(
                    "Dependencies:",
                    dependencies,
                )

        else:

            nested_routes = getattr(
                route,
                "routes",
                None,
            )

            if nested_routes:

                nested_prefix = getattr(
                    route,
                    "prefix",
                    "",
                )

                inspect_routes(
                    nested_routes,
                    prefix + nested_prefix,
                )


print()
print("===== 1. APPLICATION =====")

print(
    "FastAPI application:",
    type(app).__name__,
)

print("Application import: PASS")


print()
print("===== 2. RECURSIVE ROUTE TREE =====")

inspect_routes(app.routes)


print()
print("===== 3. OPENAPI CROSS-CHECK =====")

openapi = app.openapi()

target = "/api/v1/ai/scan"

operation = openapi.get(
    "paths",
    {},
).get(
    target,
)

print(
    "OpenAPI target:",
    target,
)

print(
    "OpenAPI operation:",
    operation is not None,
)

if operation:

    print(
        "Methods:",
        list(operation.keys()),
    )

    print(
        "Security:",
        operation.get("post", {}).get(
            "security"
        ),
    )


print()
print("===== 4. PRODUCTION SAFETY =====")

print("NO PRODUCTION SOURCE CHANGES")
print("NO GEMINI REQUEST")
print("NO DATABASE CHANGES")
print("NO QDRANT CHANGES")
print("NO EMBEDDINGS CREATED")


print()
print("=" * 80)
print("STEP 8C-003 — TASK 10B COMPLETE")
print("=" * 80)
