# tutor-buddy 🛡️

> A Claude Code skill that takes vibecoders and beginners from a raw idea to a secured,
> GitHub-ready project — without the mistakes that usually follow.

AI-assisted coding makes it dangerously easy to commit a real API key, install a package an
LLM hallucinated and an attacker then registered, build ten features before one works, or
push code that a single malicious pull request can compromise. Tutor-buddy quietly prevents
all of that — without adding ceremony or lecturing.

---

## What it is

Tutor-buddy is **not an application**. It is a Claude Code *skill*: a set of Markdown
instruction files that Claude Code loads and runs inside your project. There is no server,
no runtime, no install-time build — just a workflow that executes on top of whatever you're
building.

It runs a five-phase, gated workflow:

```text
1. Ideate  →  2. Plan  →  3. Build  →  4. Security audit  →  5. Ship to GitHub
```

Each phase is a gate. Nothing moves forward without your explicit go-ahead.

---

## How to install

**Requirements:** Claude Code with skills support.

1. **Download** `tutor-buddy.skill` from the [Releases](../../releases) page.
2. **Unzip** it — it expands to a `tutor-buddy/` folder.
3. **Place it** in a skills directory:

   ```bash
   # Global (all projects)
   mkdir -p ~/.claude/skills && mv tutor-buddy ~/.claude/skills/

   # Or project-only
   mkdir -p .claude/skills && mv tutor-buddy .claude/skills/
   ```

4. **Restart** Claude Code.

---

## How to use

You don't call it by name — it activates from what you say. Just describe what you want:

```text
I want to build a price-drop monitor that emails me alerts
I have no idea what to build — suggest something based on my background
Is this project safe to push to a public repo?
Help me put this on GitHub
```

You can enter at any phase. "I have an idea" starts at Phase 1; "is my project safe?" jumps
straight to the audit; "put this on GitHub" goes to shipping.

| What you say | Phase it enters |
| --- | --- |
| "I want to build…", "I have an idea for…" | 1 — Ideate |
| "Help me structure this", "scaffold this" | 2 — Plan |
| *(resumes after the plan is approved)* | 3 — Build |
| "Is this safe?", "audit my code" | 4 — Security audit |
| "Put this on GitHub", "help me ship this" | 5 — Ship |

When a decision is needed, tutor-buddy asks one question at a time with a sensible default.
Reply **"use the defaults"** to keep moving.

---

## The five phases

**1 · Ideate** — Bring your own idea or ask for one. Tutor-buddy stress-tests the scope,
names the riskiest assumption, and pins down the smallest version worth building — before a
line of code exists.

**2 · Plan** — Produces a written *contract*: full file/folder tree, boilerplate list, named
and pinned dependencies, a `.env.example`, and a numbered build order.

**3 · Build** — Executes only the approved plan, milestone by milestone. Deviations are
surfaced and approved, never silent. Secrets go in a gitignored `.env` from the start.

**4 · Security audit** — Runs automatically at the end of every build, and on demand. The
core idea is honest results, not a checklist that creates false confidence. Threats are split
into four groups by what an automated, build-time audit can actually verify:

| Group | What gets checked | How |
| --- | --- | --- |
| **A — Static repo checks** | Secrets in tree and git history, vulnerable deps, typosquatting, slopsquatting, dependency confusion | `gitleaks`/grep, `pip-audit`/`npm audit`/`osv-scanner`, registry lookups |
| **B — Hardening** | `.gitignore`, CI action pinning, `GITHUB_TOKEN` permissions, branch protection | Config + setup in Phase 5 |
| **C — Auth defenses** | Rate limiting, breached-password checks, session hygiene | Code inspection — only if the project has login |
| **D — Human factors** | Social engineering, phishing | Marked **NOT VERIFIABLE** — concrete habits given instead |

Group A runs once **per workspace** in monorepos. A workspace that isn't inventoried is a
workspace that never gets scanned — so the audit never emits a global PASS that hides an
unscanned workspace; it reports it as an explicit gap.

**5 · Ship** — Creates the repo (private by default), enables push protection and secret
scanning, configures branch protection against malicious PRs, and pins CI actions to commit
SHAs.

---

## What makes it different

**Slopsquatting detection.** Standard dependency audits check for known CVEs in packages
that *exist*. They don't check whether a package was real to begin with. LLMs hallucinate
plausible package names and attackers pre-register them — so tutor-buddy verifies every
direct dependency resolves to a real, established package on its registry.

**The plan is a contract.** Requiring written plan approval before code addresses the most
common vibecoding failure: scope expanding invisibly until the project is unshippable.

**Honesty over reassurance.** The audit states plainly what it cannot verify. A false green
check is worse than no check — so human-factor threats are labelled NOT VERIFIABLE rather
than rubber-stamped.

**Token-economical.** Locates before reading, reads only the relevant lines, batches
questions with defaults, and never pastes full scanner logs back at you.

---

## Repository layout

```text
SKILL.md                       # Orchestrator: stance, token rules, phase routing, Phase 3
references/
  ideation.md                  # Phase 1
  planning.md                  # Phase 2
  security-audit.md            # Phase 4 (most of the security logic)
  github-setup.md              # Phase 5
tests/
  validate.py                  # Structural checks (reference + fixture integrity)
  fixtures/                    # Sample projects with documented expected audit results
.github/workflows/ci.yml       # Runs the structural checks on every push / PR
```

`SKILL.md` is an orchestrator, not the whole skill: each heavy phase's reference file is
loaded only when that phase begins, keeping the active context small.

---

## Development & testing

There's no application to unit-test — these checks guard the *instructions*.

```bash
# Reference integrity (every references/*.md cited in SKILL.md exists, and vice versa)
# plus fixture integrity (every fixture ships an EXPECTATIONS.md). Runs in CI.
python tests/validate.py
```

**Audit fixtures** under [`tests/fixtures/`](tests/fixtures/) are tiny sample projects, each
exercising one Group A behavior with a documented `EXPECTATIONS.md`:

| Fixture | Exercises | Expected |
| --- | --- | --- |
| `01-secret-in-source` | Secret-leak detection | FAIL |
| `02-slopsquat-deps` | Typo / slopsquatting | FAIL on the bad names only |
| `03-clean-single-root` | Happy path | PASS, no false positives |
| `04-monorepo-hidden-workspace` | Monorepo inventory completeness | GAP, never a global PASS |

To validate a change to the skill, point a Claude Code session at a fixture, run the audit,
and compare the report against that fixture's `EXPECTATIONS.md`. A mismatch is a regression.
See [`tests/README.md`](tests/README.md) for details.

---

## Roadmap

- **SBOM generation** at the end of the build for a durable, portable dependency record.
- **Deployment phase** (Render, Railway, Vercel, Fly.io) with security-conscious defaults.
- **Deeper slopsquatting heuristics** — package age, maintainer reputation, name-similarity
  scoring, not just existence and download counts.
- **More stacks** — React Native / Expo, browser extensions, Tauri desktop apps.
- **Configurable strictness** — a lighter audit for prototypes, a stricter one for
  production-bound projects.

---

## Contributing

Issues and PRs welcome — blunt, reasoned feedback preferred. If you find a security check
that's missing, overclaiming, or wrong, open an issue with the reasoning. See
[Contributing.md](Contributing.md) for the bar a change has to clear.

---

## License

[MIT](LICENSE)
