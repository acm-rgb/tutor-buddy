# Expected audit result — 04-monorepo-hidden-workspace

This is the regression fixture for the false-PASS bug fixed in commit `45695a5`.

The root `package.json` declares `workspaces: ["packages/api"]` but **`packages/worker` is a
real manifest that the declared workspace globs miss**. The audit's inventory step must find
manifests by globbing the tree (ignoring `node_modules`, etc.), not by trusting the declared
`workspaces` field alone. `packages/worker` also contains a typosquatted dependency
(`requessts`), so missing it has real security cost.

```
SECURITY AUDIT - monorepo-hidden-workspace
Workspaces scanned: 2 (packages/api, packages/worker)

[workspace: packages/api]
A. Typo/slopsquatting ....... PASS  - express is real

[workspace: packages/worker]
A. Typo/slopsquatting ....... FAIL  - requessts (typo of requests)
```

Key assertions:
- The inventory must enumerate **both** `packages/api` and `packages/worker`, even though
  only `api` is in the `workspaces` field.
- The audit must **never** emit a global PASS. If for any reason `packages/worker` cannot be
  scanned, it must be reported as an explicit `GAP`, not omitted.
- A FAIL in any workspace blocks Phase 5.
