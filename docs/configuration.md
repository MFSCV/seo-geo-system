# Configuration and Distribution

[deployment.example.json](../examples/deployment.example.json) is a synthetic design example, not an executable configuration supported by an existing runner. No secret or account is configured.

## Public defaults and private overlays

| Layer | Public content | Private deployment overlay |
|---|---|---|
| Project | Schema and synthetic domains/locales/offers | Real properties, domains, native tracker and owners |
| Method | Reviewed generic policy and reference catalog | Domain-specific source/acceptance rules |
| Roles | O0/S1–S13 responsibilities | Qualified model aliases and provider terms |
| Authority | Interface and N0/N1 default | Actual mandate, writer, leases and review authorities |
| Connectors | Operation IDs and fixture behavior | Exact account/scopes, renewal, target qualification receipts |
| Scheduler | Runner interface and example timezone | Actual native task name, schedule, restart/delivery policy |
| Storage | Record schemas and retention capability | Approved location, access controls, retention/egress policy |
| Budgets | Zero paid incremental default and bounded task ceilings | Cumulative daily ledger and approved capacity |

Environment variables carry references or injected secrets only where the host supports them safely. Never commit `.env`, tokens, cookies, private signing material or a real browser session. Public profiles cannot grant authority by changing a Boolean.

## Future distributions

- `skill`: self-contained instructions, required relative references, host metadata where supported, offline helper only if included and rights-cleared.
- `offline-tools`: reproducible auditor, documented interpreter requirement, fixtures and tests; no provider credentials.
- `runtime`: Rust CLI and versioned contract/capability manifest after M2 acceptance.
- `adapter`: optional versioned integration with capability declaration, tests and qualification runbook.

Each release has a source revision, license/provenance inventory, file hashes, contract/method/adapter compatibility, test evidence and accurate implemented/unsupported status. A package with only docs is labeled a documentation release; a catalog entry is not advertised as an implemented adapter.

## Future CLI surface

These names are design targets and are not runnable today: `seo-geo audit-capture`, `seo-geo observe`, `seo-geo plan`, `seo-geo review`, `seo-geo handoff`, `seo-geo reconcile`, and `seo-geo report`. Manual and scheduled use must share the same policy, state and receipt path. No command should perform side effects merely because a credential exists.
