#!/usr/bin/env python3
import json
import sys
from pathlib import Path

# Ensure backend package root is importable when run from repository root.
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from schemas.content import AboutResponse, ExperienceResponse, ProjectsResponse


def main():
    data_root = BACKEND_ROOT / "data"
    file_to_schema = {
        "profile/about.json": AboutResponse,
        "profile/experience.json": ExperienceResponse,
        "portfolio/projects.json": ProjectsResponse,
    }

    errors = []

    json_files = sorted(
        p.relative_to(data_root).as_posix()
        for p in data_root.rglob("*.json")
    )

    # Fail unknown files to keep validation deterministic.
    unknown_files = [f for f in json_files if f not in file_to_schema]
    if unknown_files:
        for f in unknown_files:
            errors.append(f"Unknown JSON file without schema mapping: {f}")

    # Validate expected files exist.
    for rel_path in file_to_schema:
        if rel_path not in json_files:
            errors.append(f"Missing expected JSON file: {rel_path}")

    for rel_path, schema in file_to_schema.items():
        if rel_path not in json_files:
            continue

        file_path = data_root / rel_path
        try:
            with file_path.open("r", encoding="utf-8") as f:
                raw_data = json.load(f)

            payload = {
                "data": raw_data,
                "meta": {
                    "updated_at": "test",
                    "version": "v1",
                },
            }
            schema.model_validate(payload)
            print(f"[PASS] {rel_path}")
        except Exception as exc:
            errors.append(f"{rel_path}: {exc}")

    if errors:
        print("Schema validation failed:")
        for e in errors:
            print(f"- {e}")
        raise SystemExit(1)

    print("Schema validation passed")


if __name__ == "__main__":
    main()
