# Expected audit result — 03-clean-single-root

A well-formed single-root Node project: no secrets in tree, a `.env.example` with
placeholders, a `.gitignore` (shipped as `gitignore.sample`, see note below), and pinned
dependencies. This is the happy path — it exists to catch false-positive regressions.

```
A. Secrets leak ............. PASS  - no secrets; .env.example present
A. Dependency vulns ......... PASS/FAIL - per npm audit (no lockfile here → note as a gap, not a silent PASS)
A. Typo/slopsquatting ....... PASS  - express is a real, established package
A. Dependency confusion ..... N/A
B. .gitignore + CI hardening  PASS  - env, build artifacts, OS cruft covered
C. Auth defenses ............ N/A   - no login
D. Human factors ............ NOT VERIFIABLE - guidance shown
```

Key assertions:
- No secret false positive on `SESSION_SECRET=replace-me` (placeholder, not a literal secret).
- `express` is not flagged.
- Absence of a lockfile is reported as a gap, **not** silently passed.

> Note: the `.gitignore` is committed as `gitignore.sample` because the repo root
> `.gitignore` ignores nested `.gitignore` semantics in tooling; treat it as the project's
> real `.gitignore` when auditing.
