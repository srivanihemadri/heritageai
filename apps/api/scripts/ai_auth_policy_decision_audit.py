from pathlib import Path
import ast
import inspect

from app.main import app
from app.api.v1 import auth as auth_module
from app.api.v1 import users as users_module


ROOT = Path(r"D:\PROJECT\heritageai\apps\api\app")


def source(path):
    return path.read_text(encoding="utf-8")


def function_nodes(tree):
    return [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]


print("===== STEP 8B-013W-A — AUTHENTICATION POLICY DECISION AUDIT =====")


# ------------------------------------------------------------------
# 1. AUTH MODULE
# ------------------------------------------------------------------

print("\n===== 1. AUTH MODULE INSPECTION =====")

auth_path = ROOT / "api" / "v1" / "auth.py"

if not auth_path.exists():
    raise RuntimeError("auth.py not found.")

auth_source = source(auth_path)
auth_tree = ast.parse(auth_source)

print(f"Auth module: {auth_path}")
print("auth.py: PASS")

auth_functions = function_nodes(auth_tree)

for node in auth_functions:
    print(f"AUTH FUNCTION: {node.name}")

print("Auth function discovery: PASS")


# ------------------------------------------------------------------
# 2. DISCOVER SECURITY DEPENDENCIES
# ------------------------------------------------------------------

print("\n===== 2. DISCOVER AUTHENTICATION / SECURITY DEPENDENCIES =====")

security_files = []

for path in ROOT.rglob("*.py"):
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        continue

    lowered = text.lower()

    if any(
        token in lowered
        for token in [
            "get_current_user",
            "oauth2passwordbearer",
            "httpbearer",
            "security(",
            "jwt",
            "authorization",
            "bearer",
            "current_user",
        ]
    ):
        security_files.append(path)

if not security_files:
    raise RuntimeError(
        "No authentication/security implementation discovered."
    )

for path in security_files:
    print(f"SECURITY FILE: {path}")

print(f"Security-related files discovered: {len(security_files)}")
print("Security implementation discovery: PASS")


# ------------------------------------------------------------------
# 3. FIND CURRENT-USER DEPENDENCIES
# ------------------------------------------------------------------

print("\n===== 3. CURRENT USER DEPENDENCY DISCOVERY =====")

current_user_matches = []

for path in security_files:
    text = source(path)

    tree = ast.parse(text)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if (
                "current_user" in node.name.lower()
                or "auth" in node.name.lower()
                or "user" in node.name.lower()
            ):
                current_user_matches.append(
                    f"{path.name}:{node.name}"
                )

for match in current_user_matches:
    print(f"DISCOVERED: {match}")

if not current_user_matches:
    print("No obvious current-user dependency symbol discovered.")

print("Current-user dependency discovery: COMPLETE")


# ------------------------------------------------------------------
# 4. USERS ROUTER DEPENDENCY ANALYSIS
# ------------------------------------------------------------------

print("\n===== 4. USERS ROUTER AUTHORIZATION ANALYSIS =====")

users_router = getattr(users_module, "router", None)

if users_router is None:
    raise RuntimeError("Users router not found.")

for route in users_router.routes:
    path = getattr(route, "path", None)
    methods = getattr(route, "methods", set())

    if path is None:
        continue

    dependant = getattr(route, "dependant", None)

    dependencies = []

    if dependant is not None:
        for dependency in getattr(
            dependant,
            "dependencies",
            [],
        ):
            call = getattr(dependency, "call", None)

            if call is not None:
                dependencies.append(
                    getattr(
                        call,
                        "__name__",
                        repr(call),
                    )
                )

    print(
        f"USERS ROUTE: {sorted(methods)} {path} "
        f"DEPENDENCIES={dependencies}"
    )

print("Users authorization inspection: PASS")


# ------------------------------------------------------------------
# 5. AUTH ROUTER DEPENDENCY ANALYSIS
# ------------------------------------------------------------------

print("\n===== 5. AUTH ROUTER DEPENDENCY ANALYSIS =====")

auth_router = getattr(auth_module, "router", None)

if auth_router is None:
    raise RuntimeError("Auth router not found.")

for route in auth_router.routes:
    path = getattr(route, "path", None)
    methods = getattr(route, "methods", set())

    if path is None:
        continue

    dependant = getattr(route, "dependant", None)

    dependencies = []

    if dependant is not None:
        for dependency in getattr(
            dependant,
            "dependencies",
            [],
        ):
            call = getattr(dependency, "call", None)

            if call is not None:
                dependencies.append(
                    getattr(
                        call,
                        "__name__",
                        repr(call),
                    )
                )

    print(
        f"AUTH ROUTE: {sorted(methods)} {path} "
        f"DEPENDENCIES={dependencies}"
    )

print("Auth router dependency inspection: PASS")


# ------------------------------------------------------------------
# 6. OPENAPI SECURITY SCHEMES
# ------------------------------------------------------------------

print("\n===== 6. OPENAPI SECURITY SCHEME ANALYSIS =====")

openapi = app.openapi()

components = openapi.get("components", {})
security_schemes = components.get("securitySchemes", {})

print(
    f"Security schemes discovered: "
    f"{list(security_schemes.keys())}"
)

if security_schemes:
    print("OpenAPI security scheme: PRESENT")
else:
    print("OpenAPI security scheme: NOT PRESENT")

print("OpenAPI security inspection: COMPLETE")


# ------------------------------------------------------------------
# 7. PROTECTED ROUTE DETECTION
# ------------------------------------------------------------------

print("\n===== 7. PROTECTED ROUTE DETECTION =====")

protected_routes = []

for path, operations in openapi.get("paths", {}).items():
    for method, operation in operations.items():

        if method.lower() not in {
            "get",
            "post",
            "put",
            "patch",
            "delete",
        }:
            continue

        security = operation.get("security")

        if security:
            protected_routes.append(
                f"{method.upper()} {path}"
            )

for route in protected_routes:
    print(f"PROTECTED: {route}")

print(
    f"Protected OpenAPI operations: "
    f"{len(protected_routes)}"
)

print("Protected route discovery: PASS")


# ------------------------------------------------------------------
# 8. AI ENDPOINT SECURITY STATE
# ------------------------------------------------------------------

print("\n===== 8. AI ENDPOINT SECURITY STATE =====")

target = "/api/v1/ai/answer"

if target not in openapi.get("paths", {}):
    raise RuntimeError(
        f"AI endpoint missing from OpenAPI: {target}"
    )

ai_post = openapi["paths"][target].get("post")

if ai_post is None:
    raise RuntimeError(
        f"POST operation missing: {target}"
    )

ai_security = ai_post.get("security")

print(f"AI endpoint security declaration: {ai_security}")

if ai_security:
    print("AI endpoint currently documented as PROTECTED")
else:
    print("AI endpoint currently documented as PUBLIC")

print("AI endpoint security state: AUDIT COMPLETE")


# ------------------------------------------------------------------
# 9. DETERMINE EXISTING PROJECT SECURITY PATTERN
# ------------------------------------------------------------------

print("\n===== 9. EXISTING PROJECT SECURITY PATTERN =====")

protected_user_operations = [
    route
    for route in protected_routes
    if "/users" in route
]

if protected_user_operations:
    print("Existing protected user operations: PRESENT")
else:
    print("Existing protected user operations: NOT DETECTED")

auth_me_protected = any(
    "/api/v1/auth/me" in route
    for route in protected_routes
)

print(
    f"/api/v1/auth/me protected: "
    f"{auth_me_protected}"
)

print("Existing security pattern: DISCOVERED")


# ------------------------------------------------------------------
# 10. POLICY DECISION — AUDIT ONLY
# ------------------------------------------------------------------

print("\n===== 10. AI SECURITY POLICY DECISION =====")

print(
    "Current AI endpoint security state is documented above."
)

print(
    "No automatic policy change will be made."
)

print(
    "The endpoint remains unchanged pending explicit "
    "architecture decision."
)

print("Policy decision: PENDING IMPLEMENTATION")


# ------------------------------------------------------------------
# 11. PRODUCTION SAFETY
# ------------------------------------------------------------------

print("\n===== 11. PRODUCTION SAFETY =====")

print("NO PRODUCTION SOURCE CHANGES MADE.")
print("NO CONFIGURATION CHANGES MADE.")
print("NO GEMINI GENERATION CALLS MADE.")
print("NO DATABASE CHANGES MADE.")
print("NO QDRANT CHANGES MADE.")
print("NO EMBEDDINGS CREATED.")


# ------------------------------------------------------------------
# 12. FINAL STATE
# ------------------------------------------------------------------

print("\n===== STEP 8B-013W-A COMPLETE =====")

print("Authentication implementation discovery: PASS")
print("Current-user dependency discovery: PASS")
print("Auth router analysis: PASS")
print("Users router analysis: PASS")
print("OpenAPI security analysis: PASS")
print("Protected route discovery: PASS")
print("AI endpoint security state: PASS")
print("Policy decision remains implementation-pending: PASS")
print("NO PRODUCTION CHANGES MADE.")
print("DO NOT MODIFY AI AUTHENTICATION YET.")
print("SEND THE COMPLETE OUTPUT.")
