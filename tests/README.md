# tutor-buddy tests

There is no application to unit-test. These checks guard the skill's *instructions* and
provide repeatable scenarios for validating the security audit by hand.

## Structural checks (automated)

```bash
python tests/validate.py
```

Verifies reference integrity (every `references/*.md` cited in `SKILL.md` exists and vice
versa) and that every fixture ships an `EXPECTATIONS.md`. Runs in CI on every push/PR.

## Audit fixtures (manual, repeatable)

Each directory under `tests/fixtures/` is a tiny sample project that exercises one Group A
behavior of the Phase 4 security audit. Point a Claude Code session at a fixture, run the
audit ("is this project safe?"), and compare the report against that fixture's
`EXPECTATIONS.md`. A mismatch is a regression in `references/security-audit.md` or `SKILL.md`.

| Fixture | Exercises | Expected headline |
|---|---|---|
| `01-secret-in-source` | Secret leak detection (Group A) | FAIL — hardcoded key |
| `02-slopsquat-deps` | Typosquatting / slopsquatting (Group A) | FAIL — flagged packages |
| `03-clean-single-root` | Happy path, single workspace | PASS |
| `04-monorepo-hidden-workspace` | Monorepo inventory completeness | GAP, never a global PASS |

> The secrets in these fixtures are **fake and structurally invalid** — they exist only to
> trip the grep patterns in the audit. They are intentionally placed in source files rather
> than `.env`, because the repo's `.gitignore` excludes `.env`.
