# Expected audit result — 01-secret-in-source

Single-root project with a hardcoded secret in `config.py` and no `.env.example`.

```
A. Secrets leak ............. FAIL  - hardcoded sk_live / AKIA key in config.py
A. Dependency vulns ......... N/A   - no dependency manifest present
A. Typo/slopsquatting ....... N/A   - no dependency manifest present
A. Dependency confusion ..... N/A   - no internal/private packages
B. .gitignore + CI hardening  FAIL/FIXED - no .gitignore present
```

> The planted values are deliberately hyphen-broken so they trip the audit's substring
> grep (`sk_live`, `AKIA`) without matching the strict format that a real secret scanner
> validates — otherwise GitHub push protection would (correctly) block committing this
> fixture. That block actually happened once: proof the recommended defense works.

Key assertions:
- Secrets check is a **FAIL that blocks Phase 5**, not a warning.
- The audit must name the file and the matched pattern, not paste the whole file.
- It must not claim a global PASS while a Group A FAIL exists.
