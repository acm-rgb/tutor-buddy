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

## Measuring token cost

Token economy is a stated goal of the skill, so treat it like any other claim: measure it,
don't assume it. To check whether a change to `SKILL.md` or `references/security-audit.md`
made the audit cheaper or more expensive, run the **same fixture** before and after the
change and compare the session's token usage (e.g. Claude Code's `/cost`, or the usage
reported at the end of the run).

What to look for:

- Total tokens for one full audit of a fixture should trend **down or flat**, never up, for
  the same correct result.
- Coverage must be identical across the two runs — same workspaces scanned, same checks run.
  A drop in tokens that comes from skipping a check is a regression, not a win.

`04-monorepo-hidden-workspace` is the most useful fixture here: it has the most to scan, so
it best exposes both wasteful reading and an accidental coverage cut.
