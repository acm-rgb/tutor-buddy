# Expected audit result — 02-slopsquat-deps

Single-root Python project. `requirements.txt` mixes real packages with typosquatted,
near-miss, and hallucinated names.

```
A. Secrets leak ............. PASS  - no secrets in tree
A. Typo/slopsquatting ....... FAIL  - requessts, python-jwt, beautifulsoup, totally-made-up-helper
A. Dependency vulns ......... PASS/FAIL - per pip-audit on resolvable packages
A. Dependency confusion ..... N/A
```

Key assertions:
- Must flag all four bad names and **not auto-install** any of them.
- `requests` and `pyjwt` must NOT be flagged (avoid false positives on legit packages).
- The hallucinated `totally-made-up-helper` must be flagged as "does not exist on registry",
  distinct from the typo/near-miss cases.
