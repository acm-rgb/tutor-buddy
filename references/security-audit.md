# Phase 4 - Security audit

Run this automatically at the end of a build, and on demand when the user asks "is my project safe?". The point is real checks with honest results - not a checklist that creates false confidence.

The threats split into four groups by what an automated, build-time audit can actually *do* about each. Run groups A and B always. Run group C only if the project has user login. Group D cannot be verified by any audit - be explicit about that.

Produce one compact report at the end: each check as PASS / FAIL / FIXED / N/A with a one-line reason. Fix what is safely auto-fixable (after confirming); list the rest for the user.

---

## Group A - Static repo checks (always run)

**Scope - run per workspace.** Run every Group A check once per workspace root (from the monorepo inventory) and attribute each finding to its workspace. A single-root project is just the one-workspace case. Never emit a global PASS that skipped a workspace it could not scan - report that workspace explicitly as a gap. A missed scan that reads as PASS is the exact false confidence this audit exists to prevent.

**Secrets leak.** Check both the working tree and git history (secrets are often committed earlier and "deleted" later, but they stay in history).
- If `gitleaks` or `trufflehog` is installed, run it. If neither is, fall back to Grep over tracked files for high-signal patterns: `sk_live`, `AKIA`, `-----BEGIN ... PRIVATE KEY-----`, `AIza`, `xox[baprs]-`, `ghp_`, `glpat-`, plus assignments to names containing `SECRET`, `TOKEN`, `PASSWORD`, `API_KEY` with a literal value.
- Confirm `.env` is gitignored and **not** tracked (`git ls-files | grep -E '(^|/)\.env$'` must be empty). Confirm a `.env.example` with placeholders exists.
- Any real secret found is a FAIL that blocks shipping until rotated and removed from history.

**Vulnerable dependencies.** Confirm a lockfile exists and is pinned, then scan once per manifest/lockfile in the inventory: `pip-audit` (Python), `npm audit --omit=dev` (Node), `cargo audit` (Rust). `osv-scanner -r .` covers a whole tree, including all workspaces, in one pass. Report counts by severity per workspace; flag high/critical.

**Typosquatting and "slopsquatting".** This is the AI-specific risk: models hallucinate plausible package names, and attackers pre-register them. For each *direct* dependency across **all** manifests in the inventory, not just the root, verify it resolves to a real, established package on its registry. Flag: packages that do not exist, brand-new packages with near-zero downloads, and near-miss names against well-known packages (e.g. `python-jwt` vs `pyjwt`, `requessts` vs `requests`, `beautifulsoup` vs `beautifulsoup4`). Do not auto-install anything you flagged - confirm with the user first.

**Dependency confusion.** If any dependency name looks internal/private, make sure it is not also claimable on the public registry and that installs are pinned to the intended registry/scope. For a typical beginner project this is usually N/A - say so rather than inventing a finding.

## Group B - Repo and CI hardening (set up, do not just scan)

- **`.gitignore`** covers env files, secrets, build artifacts, and OS cruft. Fix if not.
- **GitHub Actions, if present** (defends against *CI/CD pipeline poisoning*): pin actions to a full commit SHA, not a moving tag like `@v4`; set top-level `permissions:` to least privilege (read-only by default); never use `pull_request_target` to check out and run untrusted PR code; never expose secrets to workflows triggered by external PRs.
- **Branch protection, required review, and CODEOWNERS** (defends against *malicious pull requests*) are configured in phase 5 - note here that they are pending.
- **Repo privacy and push protection** (reduces *source-code exfiltration* risk) are also set in phase 5; default the repo to private.

## Group C - Application auth defenses (only if the project has user login)

If there is no authentication, mark this whole group **N/A** and say why. Otherwise verify, in code:

- **Brute force:** login attempts are rate-limited / locked out / backed off after repeated failures.
- **Credential stuffing:** passwords are checked against a breached-password list (e.g. HIBP k-anonymity API) and a minimum strength; multi-factor is at least supported.
- **General auth hygiene:** passwords hashed with a slow algorithm (argon2/bcrypt, never plaintext or fast hashes like raw SHA-256); no user enumeration (same response and timing for "unknown user" vs "wrong password"); session cookies are `HttpOnly`, `Secure`, `SameSite`.

## Group D - Human factors (cannot be verified - educate, do not claim)

Social engineering and phishing target the *person*, not the code. No audit can verify protection against them, and claiming otherwise is exactly the false confidence this skill exists to prevent. State this plainly, then give the user a few concrete habits:

- Verify a package name before installing it; do not trust a name just because a model or a tutorial suggested it.
- Never paste secrets, tokens, or `.env` contents into a chat, prompt, or screen-share.
- Turn on 2FA for GitHub, npm, and PyPI accounts.
- Be suspicious of urgent messages pushing you to run a command, install a package, or click a link.

The repo controls in groups A and B reduce the blast radius if a human is fooled (least-privilege tokens, required review, push protection, no committed secrets) - but they are damage control, not prevention.

---

## Report format

```
SECURITY AUDIT - <project>
A. Secrets leak ............. PASS/FAIL/FIXED  - <reason>
A. Dependency vulns ......... PASS/FAIL        - <counts>
A. Typo/slopsquatting ....... PASS/FAIL        - <flagged pkgs>
A. Dependency confusion ..... PASS/N/A         - <reason>
B. .gitignore + CI hardening  PASS/FIXED       - <what changed>
C. Auth defenses ............ PASS/FAIL/N/A     - <reason>
D. Human factors ............ NOT VERIFIABLE    - guidance shown
```

For a monorepo, repeat the Group A lines once per workspace under a header naming the workspace, with one shared Group B/C/D section:

```
SECURITY AUDIT - <project>
Workspaces scanned: <n> (<list of workspace roots>)

[workspace: packages/api]
A. Secrets leak ............. PASS/FAIL/FIXED  - <reason>
A. Dependency vulns ......... PASS/FAIL        - <counts>
A. Typo/slopsquatting ....... PASS/FAIL        - <flagged pkgs>
A. Dependency confusion ..... PASS/N/A         - <reason>

[workspace: packages/web]
A. ...

A. Unscanned workspace ...... GAP             - <workspace + why it could not be scanned>

B. .gitignore + CI hardening  PASS/FIXED       - <what changed>
C. Auth defenses ............ PASS/FAIL/N/A     - <reason>
D. Human factors ............ NOT VERIFIABLE    - guidance shown
```

Omit the "Workspaces scanned" line for a single-root project.

If anything in group A is a FAIL involving a real secret, do not proceed to phase 5 until it is resolved.

Token note: run scanners and read their machine output yourself; report counts and the specific findings, never the full logs.
