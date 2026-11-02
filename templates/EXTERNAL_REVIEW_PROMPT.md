# Independent External Review Prompt

Use only with an authorized real provider or reviewer. Do not attribute a report before receiving it. Attach a minimized immutable packet, manifest and relevant contract/method versions.

```text
Independently review the attached SEO/GEO System packet. Identify your actual provider, model/interface or human reviewer, date, and packet hash. Do not read other reviewers' conclusions before delivering your first report.

This is a source/specification review. Do not alter code, accounts, configuration or dependencies; do not access production, credentials or personal data; do not execute code unless the packet explicitly includes authorization and a bounded test environment.

Check method/runtime boundaries, record semantics, connectors and authority, public/private separation, recovery and budgets, independent review, measurement denominators, and publication claims. Verify whether each proposed capability is implemented, documented only, historical or unknown.

For each finding give exact file/section/line, controllable input and lower-trust principal where relevant, violated boundary, concrete consequence, evidence, preconditions, confidence, and validation needed. Separate demonstrated problems, hypotheses, optional hardening and false positives.

Balance security and effectiveness. Identify the smallest effective remedy, residual risk, implementation/review cost, and effects on SEO, accessibility, latency, conversion and operation. Do not require broad restrictions without showing their benefit.

Return an English REPORT.md and findings.json. Bind conclusions to the packet hash. State exactly what you checked and what remains unknown. Do not claim a live test, provider call or production acceptance that did not occur.
```

Consolidate returned reports by evidence and cause, preserving disagreements. Model agreement is not a substitute for reproduction or competent domain acceptance.
