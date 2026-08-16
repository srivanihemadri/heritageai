from pathlib import Path

print("=" * 80)
print("STEP 8C-006 — TASK 109 DIAGNOSTIC — SCANNER VALUEERROR AUDIT")
print("=" * 80)

targets = [
    Path("app/services/ai/scanner/service.py"),
    Path("app/services/ai/scanner/contract.py"),
    Path("app/services/ai/scanner/prompts.py"),
    Path("app/services/ai/scanner/image.py"),
]

for path in targets:

    print()
    print("=" * 80)
    print(path)
    print("=" * 80)

    if not path.exists():
        print("MISSING")
        continue

    text = path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    lines = text.splitlines()

    for number, line in enumerate(lines, start=1):

        if (
            "ValueError" in line
            or "HeritageScannerResult" in line
            or "model_validate" in line
            or "model_validate_json" in line
            or "json" in line.lower()
            or "response" in line.lower()
            or "generate_content" in line
            or "parsed" in line.lower()
        ):
            start = max(1, number - 3)
            end = min(len(lines), number + 5)

            print()
            print(f"--- lines {start}-{end} ---")

            for index in range(start, end + 1):
                print(f"{index:4}: {lines[index - 1]}")


print()
print("=" * 80)
print("TASK 109 DIAGNOSTIC COMPLETE")
print("=" * 80)
print("NO GEMINI REQUEST")
print("NO DATABASE MUTATION")
print("=" * 80)
