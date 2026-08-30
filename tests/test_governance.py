"""Tests for the executable organization-governance policy."""

from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from types import ModuleType

_ROOT = Path(__file__).resolve().parents[1]


def _load_validator() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "validate_governance", _ROOT / "scripts" / "validate_governance.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("validator module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GovernanceTest(unittest.TestCase):
    """Exercise canonical and deliberately invalid maps."""

    def test_committed_governance_passes(self) -> None:
        """The committed map, profile, boundaries, and history agree."""
        validator = _load_validator()
        self.assertEqual(validator.validate_repository(_ROOT), ())

    def test_retired_name_in_active_map_is_rejected(self) -> None:
        """A historical-only identity cannot enter active/planned data."""
        validator = _load_validator()
        with tempfile.TemporaryDirectory(prefix="governance-test-") as temporary:
            root = Path(temporary) / "repo"
            shutil.copytree(_ROOT, root, ignore=shutil.ignore_patterns(".git"))
            path = root / "docs" / "repository-map.yaml"
            document = json.loads(path.read_text(encoding="utf-8"))
            document["repositories"][0]["name"] = "asc-" + "research-os"
            path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
            errors = validator.validate_repository(root)
            self.assertTrue(any("historical-only" in item for item in errors))

    def test_dependency_direction_violation_is_rejected(self) -> None:
        """The Python foundation cannot depend on its specialization."""
        validator = _load_validator()
        with tempfile.TemporaryDirectory(prefix="governance-test-") as temporary:
            root = Path(temporary) / "repo"
            shutil.copytree(_ROOT, root, ignore=shutil.ignore_patterns(".git"))
            path = root / "docs" / "repository-map.yaml"
            document = json.loads(path.read_text(encoding="utf-8"))
            for entry in document["repositories"]:
                if entry["name"] == "asc-py":
                    entry["must_not_depend_on"] = []
            path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
            errors = validator.validate_repository(root)
            self.assertTrue(any("asc-py" in item for item in errors))

    def test_xde_must_use_only_public_python_foundation(self) -> None:
        """ASC XDE cannot revert to the C++-first dependency direction."""
        validator = _load_validator()
        with tempfile.TemporaryDirectory(prefix="governance-test-") as temporary:
            root = Path(temporary) / "repo"
            shutil.copytree(_ROOT, root, ignore=shutil.ignore_patterns(".git"))
            path = root / "docs" / "repository-map.yaml"
            document = json.loads(path.read_text(encoding="utf-8"))
            for entry in document["repositories"]:
                if entry["name"] == "asc-xde":
                    entry["public_dependencies"] = ["asc-cpp"]
            path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
            errors = validator.validate_repository(root)
            self.assertTrue(any("asc-xde" in item for item in errors))

    def test_created_neural_operator_repository_cannot_be_planned(self) -> None:
        """The audited ASC NO repository cannot regress to planned metadata."""
        validator = _load_validator()
        with tempfile.TemporaryDirectory(prefix="governance-test-") as temporary:
            root = Path(temporary) / "repo"
            shutil.copytree(_ROOT, root, ignore=shutil.ignore_patterns(".git"))
            path = root / "docs" / "repository-map.yaml"
            document = json.loads(path.read_text(encoding="utf-8"))
            for entry in document["repositories"]:
                if entry["name"] == "asc-no":
                    entry["status"] = "planned"
                    entry["maturity"] = "planned"
                    entry["visibility"] = "not-created"
            path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
            errors = validator.validate_repository(root)
            self.assertTrue(any("remain planned" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
