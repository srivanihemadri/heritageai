from __future__ import annotations

from pathlib import Path
import sys
import inspect

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import app


print("=" * 80)
print("STEP 8C-003 — TASK 10C — MAIN APPLICATION ROUTER MOUNT AUDIT")
print("=" * 80)


print()
print("===== 1. MAIN.PY LOCATION =====")

import app.main as main_module

print(
    "main.py:",
    inspect.getsourcefile(main_module),
)


print()
print("===== 2. MAIN.PY SOURCE =====")

main_source = inspect.getsource(main_module)

print(main_source)


print()
print("===== 3. APPLICATION ROUTES =====")

for index, route in enumerate(app.routes, start=1):

    print()
    print(
        "ROUTE",
        index,
    )

    print(
        "Type:",
        type(route).__name__,
    )

    print(
        "Path:",
        getattr(route, "path", None),
    )

    print(
        "Name:",
        getattr(route, "name", None),
    )

    print(
        "Methods:",
        sorted(
            getattr(
                route,
                "methods",
                set(),
            )
            or set()
        ),
    )

    print(
        "Prefix:",
        getattr(
            route,
            "prefix",
            None,
        ),
    )

    print(
        "Routes attribute:",
        bool(
            getattr(
                route,
                "routes",
                None,
            )
        ),
    )


print()
print("===== 4. ROUTER IMPORT DISCOVERY =====")

for module_name in [
    "app.api.v1",
    "app.api.v1.ai",
    "app.api.v1.auth",
    "app.api.v1.users",
    "app.api.v1.heritage_sites",
]:

    try:

        module = __import__(
            module_name,
            fromlist=["*"],
        )

        print(
            module_name,
            ": IMPORT PASS",
        )

        router = getattr(
            module,
            "router",
            None,
        )

        if router is not None:

            print(
                "  router:",
                router,
            )

            print(
                "  prefix:",
                getattr(
                    router,
                    "prefix",
                    None,
                ),
            )

            print(
                "  route count:",
                len(
                    getattr(
                        router,
                        "routes",
                        [],
                    )
                ),
            )

    except Exception as exc:

        print(
            module_name,
            ": IMPORT FAIL",
            type(exc).__name__,
            str(exc),
        )


print()
print("===== 5. AI ROUTER DIRECT CHECK =====")

from app.api.v1.ai import router as ai_router

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
        "AI route:",
        getattr(route, "path", None),
        sorted(
            getattr(
                route,
                "methods",
                set(),
            )
            or set()
        ),
    )


print()
print("===== 6. OPENAPI CHECK =====")

openapi = app.openapi()

target = "/api/v1/ai/scan"

print(
    "OpenAPI target:",
    target,
)

print(
    "Present:",
    target in openapi.get(
        "paths",
        {},
    ),
)

if target in openapi.get(
    "paths",
    {},
):

    operation = openapi["paths"][target]["post"]

    print(
        "Operation ID:",
        operation.get("operationId"),
    )

    print(
        "Security:",
        operation.get("security"),
    )


print()
print("===== 7. SAFETY =====")

print("READ-ONLY AUDIT")
print("NO PRODUCTION SOURCE CHANGES")
print("NO GEMINI REQUESTS")
print("NO DATABASE CHANGES")
print("NO QDRANT CHANGES")
print("NO EMBEDDINGS CREATED")


print()
print("=" * 80)
print("STEP 8C-003 — TASK 10C COMPLETE")
print("=" * 80)
