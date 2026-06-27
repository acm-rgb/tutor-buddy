#!/usr/bin/env python3
"""Structural checks for the tutor-buddy skill.

This is not a unit-test runner for application code (there is none). It guards the
two things that silently break the skill at runtime:

  1. Reference integrity - every references/*.md cited in SKILL.md exists, and every
     file in references/ is actually cited. A renamed/dangling reference does not fail
     until a real session hits that phase; this catches it at commit time.
  2. Fixture integrity - every test fixture ships an EXPECTATIONS.md so a reviewer can
     run the audit against it and compare against a documented expected result.

Run from the repo root:  python tests/validate.py
Exit code 0 = all checks pass, 1 = at least one failure.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD = REPO_ROOT / "SKILL.md"
REFERENCES_DIR = REPO_ROOT / "references"
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"

# Matches references/<file>.md anywhere in SKILL.md (backticked, in prose, or in a path).
REFERENCE_PATTERN = re.compile(r"references/([\w.-]+\.md)")


def check_reference_integrity() -> list[str]:
    errors: list[str] = []

    if not SKILL_MD.exists():
        return [f"SKILL.md not found at {SKILL_MD}"]
    if not REFERENCES_DIR.is_dir():
        return [f"references/ directory not found at {REFERENCES_DIR}"]

    skill_text = SKILL_MD.read_text(encoding="utf-8")
    cited = set(REFERENCE_PATTERN.findall(skill_text))
    on_disk = {p.name for p in REFERENCES_DIR.glob("*.md")}

    for name in sorted(cited - on_disk):
        errors.append(f"SKILL.md cites references/{name} but the file does not exist")
    for name in sorted(on_disk - cited):
        errors.append(f"references/{name} exists but is never cited in SKILL.md")

    return errors


def check_fixture_integrity() -> list[str]:
    errors: list[str] = []

    if not FIXTURES_DIR.is_dir():
        # Fixtures are optional; absence is not a failure.
        return errors

    fixtures = [p for p in FIXTURES_DIR.iterdir() if p.is_dir()]
    for fixture in sorted(fixtures):
        if not (fixture / "EXPECTATIONS.md").exists():
            errors.append(
                f"fixture {fixture.relative_to(REPO_ROOT)} is missing EXPECTATIONS.md"
            )

    return errors


def main() -> int:
    all_errors: list[str] = []
    all_errors += check_reference_integrity()
    all_errors += check_fixture_integrity()

    if all_errors:
        print("FAIL - tutor-buddy structural checks")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print("PASS - reference and fixture integrity OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
