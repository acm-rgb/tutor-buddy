# tutor-buddy 🛡️

> A Claude Code skill that takes vibecoders and beginners from raw idea to a secured, GitHub-ready project — without the mistakes that usually follow.

AI-assisted coding makes it dangerously easy to commit a real API key, install a package that was hallucinated and then registered by an attacker, build ten features before one works, or push code that a single malicious pull request can compromise. Tutor-buddy exists to quietly prevent all of that, without adding ceremony or lecturing.

---

## Technologies Used

- **[Claude Code](https://docs.anthropic.com/claude-code)** — the runtime that executes skills and reads the project's file system
- **Claude Code Skills API** — the `.skill` format (a structured zip of Markdown instructions and reference files) that Claude Code loads and triggers contextually
- **`gitleaks` / `trufflehog`** (optional) — secret scanners invoked in the audit phase
- **`pip-audit` / `npm audit` / `osv-scanner`** — dependency vulnerability scanners, used conditionally per stack
- **GitHub CLI (`gh`)** — used in the ship phase to create repos, set branch protection, and enable push protection non-interactively

No application runtime is required. Tutor-buddy is pure instruction — a workflow that runs inside Claude Code on top of your project.

---

## Features

**Five-phase guided workflow**

```
Ideate → Plan → Build → Security Audit → Ship
```

Each phase is a gate. Nothing moves forward without explicit approval.

**Idea engine**  
Bring your own idea or ask for suggestions. Tutor-buddy stress-tests scope, identifies the riskiest assumption, and pins down the smallest version worth building — before a single line of code is written.

**Contract-driven build**  
The plan phase produces a full file/folder tree, boilerplate list, named and pinned dependencies, a `.env.example`, and a numbered build order. The build phase executes only that plan. Deviations are surfaced and approved, never silent.

**Honest security audit**  
Runs automatically at the end of every build. Threats are split by what can actually be verified at build time versus what cannot — and the distinction is stated plainly:

| Group | What gets checked | How |
|---|---|---|
| A — Repo static checks | Secrets in tree and git history, vulnerable deps, typosquatting, slopsquatting, dependency confusion | `gitleaks`/grep, `pip-audit`/`npm audit`, registry lookups |
| B — Hardening | `.gitignore`, CI action pinning, `GITHUB_TOKEN` permissions, branch protection | Automated config + setup in phase 5 |
| C — Auth defenses | Rate limiting, breached-password checks, session hygiene | Code inspection — only if the project has login |
| D — Human factors | Social engineering, phishing | Marked NOT VERIFIABLE. Three concrete habits given instead. |

**Slopsquatting detection**  
A specific risk in AI-assisted development: language models hallucinate plausible package names, and attackers pre-register them. Tutor-buddy checks that every direct dependency resolves to a real, established package on its registry.

**Hardened GitHub setup**  
Creates the repo (private by default), enables push protection and secret scanning, configures branch protection against malicious pull requests, and pins CI action versions to commit SHAs.

**Token-economical**  
Locates before reading, reads only relevant lines, batches questions with sensible defaults, never pastes full scanner logs back at you.

---

## Keyboard Shortcuts / Trigger Phrases

Tutor-buddy activates automatically — no need to call it by name. Natural phrases that trigger the skill:

| What you say | Phase it enters |
|---|---|
| "I want to build...", "I have an idea for..." | Phase 1 — Ideate |
| "Help me structure this project", "scaffold this" | Phase 2 — Plan |
| Resumes after plan is approved | Phase 3 — Build |
| "Is this project safe?", "audit my code" | Phase 4 — Security audit |
| "Put this on GitHub", "help me ship this" | Phase 5 — Ship |

You can jump into any phase. If you already have a project, "is my project safe?" skips straight to the audit.

---

## The Process

The core problem was that beginner-focused AI coding workflows tend to fall into one of two failure modes: they are either so permissive that they rubber-stamp bad decisions (leaked secrets, hallucinated packages, scope creep), or so process-heavy that the user gives up before shipping anything.

The design goal was a workflow with genuine discipline but minimal friction.

**Phase separation as a contract mechanism.** The plan phase produces a written contract. The build phase is not allowed to deviate from it silently. This addresses the most common vibecoding failure: scope expanding invisibly during a session until the project is unshippable.

**Threat classification in the security audit.** The first design decision was to stop treating all attack vectors as equivalent. Some threats — secret leaks, vulnerable dependencies, typosquatted packages — can be verified and fixed by tooling at build time. Others, like CI pipeline poisoning, are configuration choices that the tooling sets up rather than scans. Auth defenses only apply if the project has authentication, so treating them as universal produces false findings. Human-layer attacks (phishing, social engineering) cannot be verified by any audit, and claiming otherwise creates exactly the false confidence the skill is designed to prevent. Each group was assigned the right treatment rather than the same treatment.

**Slopsquatting as a first-class concern.** Standard dependency audits check for known CVEs in packages that exist. They do not check whether the package was real to begin with. In AI-assisted development, a hallucinated package name that an attacker has pre-registered is a credible supply chain risk, and it required an explicit check separate from the CVE scan.

**Progressive disclosure for token economy.** The `SKILL.md` orchestrates the workflow but does not contain all of it. Each heavy phase has a reference file loaded only when that phase begins, keeping the active context small across the session.

**Honesty as a design principle.** The skill explicitly tells the user what it cannot verify. This is a constraint on the content of the audit report, not just a disclaimer. A false green check is worse than no check.

---

## What We Learned

**Threat categorization matters more than threat volume.** A checklist of 11 attack vectors sounds thorough. Most checklists apply the same treatment to all of them — scan, check, pass/fail. The useful insight was that the right response to social engineering is fundamentally different from the right response to a secret leak, and mixing them into the same category produces either false confidence or useless noise.

**The build contract solves a workflow problem, not just a technical one.** Requiring written plan approval before writing code sounds like overhead. In practice, it addresses the reason most vibe-built projects stall: the user and the assistant accumulate implicit decisions that neither has fully committed to, and the project quietly becomes incoherent. Making the plan explicit and requiring a signature forces the incoherence to surface before it is baked into the code.

**Token economy is a UX concern, not just a cost concern.** A skill that reads whole files when it needs three lines, or dumps scanner output verbatim, creates a noisy session that discourages engagement. Treating tokens as a budget — locate before reading, summarize findings rather than pasting them — keeps the interaction fast and readable for a beginner audience.

---

## How It Could Be Improved

- **SBOM generation.** Producing a software bill of materials at the end of the build phase would make the dependency audit more durable and portable.
- **Deployment phase.** The current workflow ends at GitHub. A phase 6 covering common deployment targets (Render, Railway, Vercel, Fly.io) with security-conscious defaults would complete the pipeline.
- **Deeper slopsquatting heuristics.** Currently checks for package existence and approximate download counts. A more robust check would include age, maintainer reputation, and similarity score against known legitimate packages.
- **Stack expansion.** Current defaults cover the most common beginner stacks. Mobile (React Native / Expo), browser extensions, and desktop apps (Tauri) are not yet covered.
- **Configurable strictness.** A flag to run a lighter audit for rapid prototyping versus a stricter one for production-bound projects would let the same skill serve different stages of a project's lifecycle.

---

## How to Run / Install

**Requirements:** Claude Code with skills support.

**1. Download**  
Get `tutor-buddy.skill` from the [Releases](../../releases) page.

**2. Install**  
Unzip the `.skill` file — it expands to a `tutor-buddy/` folder. Place it in your skills directory:

```bash
# Global (available in all projects)
mkdir -p ~/.claude/skills
mv tutor-buddy ~/.claude/skills/

# Or project-only
mkdir -p .claude/skills
mv tutor-buddy .claude/skills/
```

**3. Restart Claude Code**

**4. Use it**  
No invocation needed. Just describe what you want to build:

```
I want to build a price-drop monitor that emails me alerts
```

```
I have no idea what to build — suggest something based on my background
```

```
Is this project safe to push to a public repo?
```

```
Help me put this on GitHub
```

When a decision is needed, tutor-buddy asks one question at a time with a default. Reply "use the defaults" to keep moving.

---

## Contributing

Issues and PRs are welcome. If you find a security check that should be added, one that is overclaiming, or a stack that should be in the defaults, open an issue with the reasoning. Blunt feedback preferred.

---

## License

MIT