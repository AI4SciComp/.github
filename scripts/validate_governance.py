"""Validate organization repository-map and canonical-name policy."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any, cast

_EXPECTED_NAMES = {
    ".github",
    "asc-cmake",
    "asc-cpp",
    "asc-devtools",
    "asc-kinetic",
    "asc-lean",
    "asc-no",
    "asc-os",
    "asc-py",
    "asc-xde",
}
_HISTORICAL_ONLY = {
    "asc-" + "research-os",
    "asc-" + "xde-py",
    "asc-" + "mathcopilot",
    "asc-" + "lab",
}
_STATUSES = {"active", "planned", "archived"}
_MATURITIES = {"governance", "foundation", "implemented", "skeleton", "planned"}
_VISIBILITIES = {"public", "private", "not-created"}
_PLANES = {"research", "scientific-computing", "engineering"}
_REQUIRED_FIELDS = {
    "name",
    "status",
    "maturity",
    "visibility",
    "plane",
    "role",
    "languages",
    "public_dependencies",
    "build_dependencies",
    "research_sidecar",
    "must_not_depend_on",
}


def _read_object(path: Path) -> dict[str, Any]:
    """Read a JSON-compatible YAML document as a mapping."""
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(
            f"{path}: invalid UTF-8 JSON-compatible YAML: {error}"
        ) from error
    if not isinstance(document, dict):
        raise TypeError(f"{path}: root must be a mapping")
    return cast(dict[str, Any], document)


def _string_list(value: object, field: str, name: str) -> list[str]:
    """Require a unique list of strings."""
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise TypeError(f"{name}.{field}: expected a string list")
    typed = cast(list[str], value)
    if len(typed) != len(set(typed)):
        raise ValueError(f"{name}.{field}: duplicate values are forbidden")
    return typed


def _validate_entry(entry: object) -> dict[str, Any]:
    """Validate one map entry and return its typed mapping."""
    if not isinstance(entry, dict):
        raise TypeError("each repositories item must be a mapping")
    typed = cast(dict[str, Any], entry)
    name = typed.get("name")
    if not isinstance(name, str):
        raise TypeError("repository name must be a string")
    fields = set(typed)
    if fields != _REQUIRED_FIELDS:
        missing = sorted(_REQUIRED_FIELDS - fields)
        extra = sorted(fields - _REQUIRED_FIELDS)
        raise ValueError(f"{name}: fields differ; missing={missing}, extra={extra}")
    if typed["status"] not in _STATUSES:
        raise ValueError(f"{name}: invalid status")
    if typed["maturity"] not in _MATURITIES:
        raise ValueError(f"{name}: invalid maturity")
    if typed["visibility"] not in _VISIBILITIES:
        raise ValueError(f"{name}: invalid visibility")
    if typed["plane"] not in _PLANES:
        raise ValueError(f"{name}: invalid plane")
    if not isinstance(typed["role"], str) or not typed["role"].strip():
        raise ValueError(f"{name}: role must be non-empty")
    for field in (
        "languages",
        "public_dependencies",
        "build_dependencies",
        "must_not_depend_on",
    ):
        _string_list(typed[field], field, name)
    sidecar = typed["research_sidecar"]
    if sidecar is not None and not isinstance(sidecar, str):
        raise TypeError(f"{name}.research_sidecar: expected string or null")
    return typed


def validate_repository(root: Path) -> tuple[str, ...]:
    """Return all governance validation failures in stable order."""
    errors: list[str] = []
    map_path = root / "docs" / "repository-map.yaml"
    try:
        document = _read_object(map_path)
        schema = _read_object(root / "docs" / "repository-map.schema.json")
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append("repository-map schema must declare Draft 2020-12")
        if document.get("schema_version") != "ai4scicomp.repository-map/v1":
            errors.append("repository-map schema_version is not v1")
        raw_entries = document.get("repositories")
        if not isinstance(raw_entries, list):
            raise TypeError("repositories must be a list")
        entries = [_validate_entry(item) for item in raw_entries]
    except (TypeError, ValueError) as error:
        return (str(error),)

    names = [cast(str, entry["name"]) for entry in entries]
    if len(names) != len(set(names)):
        errors.append("repository names must be unique")
    if names != sorted(names):
        errors.append("repository entries must use canonical name order")
    if set(names) != _EXPECTED_NAMES:
        errors.append(
            "repository set differs: "
            f"missing={sorted(_EXPECTED_NAMES - set(names))}, "
            f"extra={sorted(set(names) - _EXPECTED_NAMES)}"
        )
    for entry in entries:
        name = cast(str, entry["name"])
        if name in _HISTORICAL_ONLY:
            errors.append(f"historical-only name appears in map: {name}")
        if name in cast(Sequence[str], entry["public_dependencies"]):
            errors.append(f"{name}: self public-dependency")
        if name in cast(Sequence[str], entry["build_dependencies"]):
            errors.append(f"{name}: self build-dependency")

    indexed = {cast(str, entry["name"]): entry for entry in entries}
    planned = {name for name, entry in indexed.items() if entry["status"] == "planned"}
    if planned != {"asc-no"}:
        errors.append(f"only asc-no may be planned, found {sorted(planned)}")
    neural = indexed.get("asc-no", {})
    if neural.get("visibility") != "not-created":
        errors.append("asc-no must remain explicitly not-created")
    if neural.get("public_dependencies") != ["asc-py"]:
        errors.append("asc-no must depend only on released asc-py at repository level")
    if "asc-os-runtime" not in neural.get("must_not_depend_on", []):
        errors.append("asc-no must prohibit an asc-os runtime dependency")
    research = indexed.get("asc-os", {})
    if research.get("public_dependencies") or research.get("build_dependencies"):
        errors.append("asc-os must have no repository runtime/build dependencies")
    if not {"asc-cpp", "asc-py", "asc-no"}.issubset(
        set(research.get("must_not_depend_on", []))
    ):
        errors.append("asc-os must prohibit numerical runtime dependencies")
    for foundation in ("asc-cpp", "asc-py"):
        prohibited = set(indexed.get(foundation, {}).get("must_not_depend_on", []))
        if not {"asc-os", "asc-no"}.issubset(prohibited):
            errors.append(
                f"{foundation}: downstream/research dependency prohibition missing"
            )

    active_documents = [
        root / "README.md",
        root / "profile" / "README.md",
        root / "docs" / "architecture.md",
        root / "docs" / "repository-boundaries.md",
        root / "docs" / "research-lifecycle.md",
        map_path,
    ]
    for path in active_documents:
        text = path.read_text(encoding="utf-8")
        errors.extend(
            f"historical-only name {name} appears in active document {path.relative_to(root)}"
            for name in sorted(_HISTORICAL_ONLY)
            if name in text
        )
    history = (root / "docs" / "name-migrations.md").read_text(encoding="utf-8")
    for name in sorted(_HISTORICAL_ONLY):
        if name not in history:
            errors.append(f"historical migration evidence missing for {name}")
    profile = (root / "profile" / "README.md").read_text(encoding="utf-8")
    if "`asc-no` is\n  planned" not in profile:
        errors.append("organization profile must label asc-no as planned")
    return tuple(sorted(errors))


def main() -> int:
    """Validate the repository containing this script."""
    root = Path(__file__).resolve().parents[1]
    errors = validate_repository(root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("organization governance and repository-map validation: passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
