# Phase 2 - Plan

Goal: a complete, written plan the user approves *before* any code is written. The plan is the contract for the build phase.

## Step 1: Pick the stack

Default to a small set of proven stacks. Match the project, justify the choice in one line, and do not over-engineer. If the project does not fit any of these, ask before inventing something exotic.

| Project shape | Default stack | Why |
|---|---|---|
| Static or marketing site, simple interactivity | Plain HTML/CSS/JS, or Astro if multi-page | No build complexity to trip over |
| Web app with a backend, user is Python-leaning | FastAPI + SQLite (Postgres if it must scale) + a minimal frontend | One language, fast to run locally |
| Full-stack app needing auth + DB quickly, JS-leaning | Next.js (App Router) + Postgres (SQLite locally) | Auth/DB patterns are well-trodden |
| Command-line tool | Python with Typer, or Node with a small CLI lib | Minimal surface area |
| Data or ML script | Python + venv/uv, pinned requirements | Reproducible |

Pin dependency versions. Prefer the smallest dependency set that does the job - every dependency is attack surface and a thing to maintain.

## Step 2: Write the plan

Produce all of this before coding:

- **File/folder tree** with every file named and a one-line note on what each does.
- **Boilerplate to scaffold:** the exact starter files (entry point, config, `.gitignore`, `.env.example`, README stub).
- **Dependencies:** each one named and version-pinned, with a word on why it is needed.
- **Environment variables:** listed as `.env.example` placeholders. Never put real values in the plan.
- **Build order:** numbered milestones, each small and independently runnable. This is the sequence the build phase follows.

## Step 3: Ask only what changes the plan

When something is genuinely ambiguous and affects structure, ask - but batch the questions and give each a sensible default so the user can reply "use the defaults." Do not ask about things that do not change the plan. Examples worth asking: data persistence (file vs database), whether there are user accounts (this decides whether the auth security checks in phase 4 even apply), and deployment target if it shapes the structure.

## Step 4: Confirm

Show the tree, the milestones, and the dependency list. Get an explicit go-ahead. Then move to build and follow the plan exactly.

Token note: the tree and milestones can be terse. One line per file, one line per milestone.
