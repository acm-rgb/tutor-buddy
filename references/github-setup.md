# Phase 5 - Ship to GitHub

Goal: get the project onto GitHub safely, with the repo hardened. Never reach this phase with an unresolved secret leak from the audit.

## Step 0: Pre-push gate

Confirm two things before anything is pushed:
- The phase-4 secrets check passed (no real secret in tree or history).
- `.env` is gitignored and not tracked.

If either fails, stop and fix first. A pushed secret must be treated as compromised and rotated, not just deleted.

## Step 1: Repo files

Make sure these exist (create the missing ones):
- `.gitignore` (verified in phase 4)
- `.env.example` with placeholder values
- `README.md` - what it is, why, how to set up, how to run
- `LICENSE` - ask which; default to MIT for a beginner unless they say otherwise
- `CODEOWNERS` and a short `CONTRIBUTING.md` only if the project expects collaborators

## Step 2: Local git

```bash
git init        # if not already a repo
git add -A
git status      # confirm no .env or secret files are staged
git commit -m "Initial commit"
git branch -M main
```

Eyeball `git status` output for stray secret/credential files before the first commit.

## Step 3: Create the remote

If the GitHub CLI is available and authenticated (`gh auth status`):

```bash
gh repo create <name> --private --source=. --remote=origin --push
```

Default to **private**. Only make it public if the user explicitly chooses to, and only after the audit passed.

If `gh` is not installed or not authenticated, do not assume - give the exact manual steps instead: create the repo on github.com, then

```bash
git remote add origin https://github.com/<user>/<name>.git
git push -u origin main
```

## Step 4: Harden the remote

Via `gh`/the API if available, otherwise as a short checklist for the user to click through in repo Settings:
- Enable **secret scanning** and **push protection** (blocks future secret pushes).
- Enable **branch protection** on `main`: require a pull request and at least one review before merge (defends against malicious PRs).
- Set the default Actions `GITHUB_TOKEN` permissions to read-only.

## Step 5: Optional minimal CI

Only if the project actually has tests or linting set up. A small workflow that runs them on PRs - with actions pinned to commit SHAs and least-privilege `permissions:`. Do not add CI ceremony for a project that has nothing to run.

## Step 6: Final summary

Print the repo URL and a three-line close:
- What is protected (private repo, no committed secrets, push protection, branch protection).
- What is still on the user (the human-factor habits from the audit's group D).
- The next concrete step (e.g. "share the repo link" or "set up deployment").

Token note: use `gh` non-interactive flags, do not poll, and give one summary at the end rather than narrating each command.
