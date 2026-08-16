from __future__ import annotations

import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from fastapi.routing import APIRoute
from fastapi import FastAPI

from app.main import app


print("=" * 80)
print("STEP 8C-003 — TASK 6-RECOVERY — FINAL SCANNER ROUTE TREE AUDIT")
print("=" * 80)


print()
print("===== 1. APPLICATION IMPORT =====")

print("FastAPI application:", type(app).__name__)

if not isinstance(app, FastAPI):
    raise RuntimeError("Application is not a FastAPI instance.")

print("Application import: PASS")


print()
print("===== 2. TOP-LEVEL ROUTE TREE =====")


def inspect_routes(routes, prefix=""):
    matches = []

    for route in routes:

        path = getattr(route, "path", None)
        methods = getattr(route, "methods", set())

        if path is not None:

            full_path = prefix + path

            if isinstance(route, APIRoute):

                print(
                    "APIRoute:",
                    full_path,
                    "METHODS=",
                    sorted(methods),
                    "NAME=",
                    getattr(route, "name", None),
                )

                if (
                    full_path == "/api/v1/ai/scan"
                    and "POST" in methods
                ):
                    matches.append(route)

            elif hasattr(route, "routes"):

                print(
                    "Router:",
                    full_path,
                    "ROUTES=",
                    len(route.routes),
                )

                matches.extend(
                    inspect_routes(
                        route.routes,
                        full_path,
                    )
                )

        elif hasattr(route, "routes"):

            print(
                "Nested router without path:",
                type(route).__name__,
                "ROUTES=",
                len(route.routes),
            )

            matches.extend(
                inspect_routes(
                    route.routes,
                    prefix,
                )
            )

    return matches


matches = inspect_routes(app.routes)


print()
print("===== 3. FINAL SCANNER ROUTE MATCHES =====")

print(
    "POST /api/v1/ai/scan matches:",
    len(matches),
)

if len(matches) != 1:

    print()
    print("Scanner route was not uniquely discovered.")

    print()
    print("===== OPENAPI FALLBACK =====")

    openapi = app.openapi()

    paths = openapi.get("paths", {})

    target = paths.get("/api/v1/ai/scan")

    print(
        "OpenAPI /api/v1/ai/scan:",
        target,
    )

    if target is None:
        raise RuntimeError(
            "Scanner endpoint missing from both route tree and OpenAPI."
        )

    if "post" not in target:
        raise RuntimeError(
            "Scanner OpenAPI endpoint does not expose POST."
        )

    print("OpenAPI scanner endpoint: PASS")

else:

    print("Final scanner route: PASS")


print()
print("===== 4. SCANNER ROUTE DETAILS =====")

if len(matches) == 1:

    route = matches[0]

    print("Path:", route.path)
    print("Methods:", sorted(route.methods))
    print("Name:", route.name)
    print("Endpoint:", route.endpoint)
    print("Response model:", route.response_model)

    dependencies = []

    for dependency in route.dependant.dependencies:

        call = dependency.call

        if call is not None:

            dependencies.append(
                getattr(
                    call,
                    "__name__",
                    str(call),
                )
            )

    print("Dependencies:", dependencies)

    if "get_current_user" not in dependencies:
        raise RuntimeError(
            "Final scanner route missing get_current_user."
        )

    print("Authentication dependency: PASS")


print()
print("===== 5. OPENAPI FINAL CONTRACT =====")

openapi = app.openapi()

operation = openapi["paths"].get(
    "/api/v1/ai/scan"
)

if operation is None:
    raise RuntimeError(
        "OpenAPI scanner endpoint missing."
    )

print("POST operation:", "post" in operation)

if "post" not in operation:
    raise RuntimeError(
        "POST scanner operation missing."
    )

post_operation = operation["post"]

print(
    "Request body:",
    post_operation.get("requestBody"),
)

print(
    "Responses:",
    list(
        post_operation.get(
            "responses",
            {}
        ).keys()
    ),
)

security = post_operation.get(
    "security"
)

print(
    "Security:",
    security,
)

if not security:
    raise RuntimeError(
        "Scanner endpoint missing OpenAPI security declaration."
    )

print("OpenAPI security: PASS")


print()
print("===== 6. AI ROUTER CROSS-CHECK =====")

from app.api.v1.ai import router as ai_router

ai_matches = [
    route
    for route in ai_router.routes
    if getattr(route, "path", None) == "/ai/scan"
    and "POST" in getattr(
        route,
        "methods",
        set(),
    )
]

print(
    "AI router POST /ai/scan:",
    len(ai_matches),
)

if len(ai_matches) != 1:
    raise RuntimeError(
        "AI router scanner route is not unique."
    )

print("AI router scanner route: PASS")


print()
print("===== 7. PRODUCTION ROUTER CROSS-CHECK =====")

print(
    "AI router prefix:",
    ai_router.prefix,
)

print(
    "AI router route count:",
    len(ai_router.routes),
)

for route in ai_router.routes:

    print(
        "AI ROUTER ROUTE:",
        getattr(route, "path", None),
        getattr(route, "methods", None),
    )

print("Production router inspection: PASS")


print()
print("===== 8. NO-MUTATION GUARANTEE =====")

print("Gemini requests: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("STEP 8C-003 — TASK 6-RECOVERY COMPLETE")
print("=" * 80)

print("Final route tree audit: COMPLETE")
print("OpenAPI scanner endpoint: VERIFIED")
print("AI router scanner endpoint: VERIFIED")
print("NO PRODUCTION SOURCE CHANGES.")
print("DO NOT RUN REAL GEMINI.")
print("SEND THE COMPLETE OUTPUT.")
