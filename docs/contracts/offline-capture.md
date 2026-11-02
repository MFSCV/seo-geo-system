# Offline Capture Compatibility

The archived skill contains `scripts/audit_snapshot.py` and `scripts/test_audit_snapshot.py`. The future public paths are `tools/offline-capture/audit_snapshot.py` and `tests/offline-capture/test_audit_snapshot.py`.

Retain the existing input shape: exactly one of `document` or `documents`; each captured document records URL, optional HTTP status/headers, captured HTML and expected canonical/indexability/locale where supplied. Missing headers mean unobserved headers, not a verified empty set.

Preserve exit codes: **0** means no captured error findings; **1** means captured error findings; **2** means invalid input or invocation. Output scope remains `offline-capture-not-live`. Optional output remains create-only, preventing accidental overwrite.

The compatibility bridge adds the shared envelope without changing the legacy payload or silently reinterpreting its severity. URL query/fragment redaction and all existing negative/invalid-input behaviors remain protected by the original tests. New envelope fields are derived from known capture metadata or explicitly marked unknown.

An offline capture cannot prove present reachability, complete response headers, semantic or clinical truth, consent, rich-result eligibility, index state, ranking or publication authority. A successful audit is useful evidence within its scope, not an approval for a website release.

The reviewed source tests are recorded in [source reconciliation](../source-reconciliation.md). They must be rerun against the extracted release revision during M1; historical success is not inherited after code changes.
