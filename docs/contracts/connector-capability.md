# Connector Capability and Qualification Contract

Catalog existence, implemented code, available tooling, account authentication, correct property scope, read qualification, write qualification, live propagation, and recurring operation are independent dimensions. An overall `connected=true` flag is insufficient.

A binding includes provider and adapter version; deployment/environment; principal reference; project/property/site; exact operation ID; read/write effect; permitted fields/targets; authority reference; credential reference; supported transport; contract/documentation revision; pagination; quotas/cost; source lag; retention/egress; idempotency/CAS support; and error/receipt semantics.

Do not export actual account or token references to the public catalog. The public registry describes operation semantics; private qualification records describe the deployment's access and evidence.

## Qualification evidence

| Dimension | Evidence required | Failure behavior |
|---|---|---|
| Documentation | Exact supported method/schema and current source | Unsupported/unknown; no invented endpoint |
| Implementation | Adapter revision and fixture tests | Catalog-only; retain manual/export path |
| Authentication | Actual intended principal and renewal/revocation behavior | Unavailable; no borrowed browser session assumption |
| Target scope | Exact property/site/environment and permitted fields | Deny mismatched target |
| Read | Minimal real result, completeness/period and sanitized receipt | Unknown rather than zero |
| Write | Exact effect, mandate, baseline, per-item result, recovery exercise | Proposal only until qualified |
| Propagation | Actual public output or intended native effect | Applied but unverified, or unknown |
| Recurrence | Runner, renewable auth, timezone/DST, restart, quota and alert evidence | Manual mode only |

No write is enabled just because a read works. No recurring job is installed by importing the skill. Documentation of a dashboard report does not prove an API exists for it. Google/Bing reports, consumer assistant interfaces and model APIs retain separate cohorts and capability states.

## Error semantics

401/expired credentials use the supported renewal path only. 403 identifies missing permission and stops the affected operation. 429 respects current `Retry-After`, quota and bounded backoff. Safe-read timeouts can receive bounded retries; the result remains unknown if collection fails. Write timeouts or partial bulk results enter reconciliation before any retry. Revision drift or lease expiry blocks the stale patch, preserving the candidate for rebase.

Public fetching validates allowed origins, every redirect and resolved destination, request count, bytes, depth and duration. Do not forward authenticated cookies across origins. Private networks, metadata endpoints and customer/clinical areas are outside public crawling. Browser interaction is used only for an authorized task and permitted fallback; it is not a hidden workaround for insufficient service scopes.

The full reconciliation is in [connector operations](../../catalog/connector-operations.csv) and [source crosswalk](../../catalog/connector-crosswalk.csv).
