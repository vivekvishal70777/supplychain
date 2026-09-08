#!/usr/bin/env python3
"""Validate XML, YAML, JSON, and RAML files without requiring Mule EE."""
from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def check_xml(path: Path) -> None:
    try:
        ET.parse(path)
    except ET.ParseError as exc:
        ERRORS.append(f"XML {path}: {exc}")


def check_json(path: Path) -> None:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        ERRORS.append(f"JSON {path}: {exc}")


def check_yaml_indent(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "\t" in text:
        ERRORS.append(f"YAML {path}: contains tabs")
    try:
        import yaml  # type: ignore

        yaml.safe_load(text)
    except ImportError:
        # Structural check only: every non-empty, non-comment line must contain ':' or start a list.
        for i, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped.startswith("- "):
                continue
            if ":" not in stripped:
                ERRORS.append(f"YAML {path}:{i}: missing ':' in '{stripped}'")
    except Exception as exc:  # PyYAML present but invalid
        ERRORS.append(f"YAML {path}: {exc}")


def check_raml(path: Path) -> None:
    first = path.read_text(encoding="utf-8").lstrip().splitlines()[0]
    if not first.startswith("#%RAML"):
        ERRORS.append(f"RAML {path}: missing #%RAML header")


def main() -> int:
    for path in ROOT.rglob("*"):
        if "target" in path.parts or ".git" in path.parts:
            continue
        if not path.is_file():
            continue
        if path.suffix == ".xml":
            check_xml(path)
        elif path.suffix == ".json":
            check_json(path)
        elif path.suffix in {".yaml", ".yml"}:
            check_yaml_indent(path)
        elif path.suffix == ".raml":
            check_raml(path)
    if ERRORS:
        print("VALIDATION FAILED")
        for err in ERRORS:
            print(" -", err)
        return 1
    print("All XML/JSON/YAML/RAML artifacts validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
