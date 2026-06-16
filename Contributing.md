# Contributing to tutor-buddy

Thanks for taking the time. Blunt, reasoned feedback is preferred over enthusiasm — if something is wrong or missing, say so directly and explain why.

---

## What we are looking for

**High-value contributions:**

- Security checks that are missing, overclaiming, or wrong — with a concrete explanation of what the correct behavior should be
- Stack defaults that are missing or poorly chosen for the target audience (beginners, vibecoders)
- Trigger phrases that should activate the skill but don't
- Cases where the skill produces false confidence (claims to verify something it cannot)
- New reference files for phases that need more depth

**Lower priority:**

- Cosmetic changes to wording
- Adding stacks that are niche or require significant prior knowledge to use safely
- Expanding the scope beyond the five-phase workflow without a strong reason

---

## How to contribute

1. **Open an issue first** for anything non-trivial. Describe the problem, the proposed change, and the tradeoff. Get a response before writing code.
2. **Fork the repo** and create a branch from `main`.
3. **Make your changes** to the relevant `.md` file inside the skill folder.
4. **Test it** — install the modified skill in Claude Code and run at least one realistic session through the affected phase.
5. **Open a pull request** with a clear title and a short description of what changed and why.

---

## Skill file structure

```
tutor-buddy/
├── SKILL.md                     # Main orchestrator — phases, stance, token rules
└── references/
    ├── ideation.md              # Phase 1
    ├── planning.md              # Phase 2
    ├── security-audit.md        # Phase 4 — most likely place for security contributions
    └── github-setup.md          # Phase 5
```

Phase 3 (Build) is behavioral and lives inside `SKILL.md` directly — no separate file.

Reference files are loaded only when their phase begins, so keep them self-contained and focused on their phase.

---

## Editing guidelines

- Write in the imperative ("Run the scan", not "You should run the scan").
- One claim per sentence. If a sentence needs "and", consider splitting it.
- When adding a security check: state what it detects, how it detects it (exact command or grep pattern), and what the correct response to a finding is. Do not add checks without all three.
- When marking something NOT VERIFIABLE, explain why in one sentence. Do not soften it.
- Keep token economy in mind: instructions that cause Claude to read large files unnecessarily, repeat information, or produce verbose output are bugs, not style choices.

---

## What gets rejected

- Changes that make the security audit less honest (softening NOT VERIFIABLE labels, adding vague checks without concrete tooling).
- Scope expansion that makes the workflow heavier for the beginner audience without a clear payoff.
- PRs opened without a prior issue for non-trivial changes.

---

## License

By contributing, you agree that your contributions will be licensed under the same [MIT License](LICENSE) that covers this project.