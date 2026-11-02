# Operations, Recurrence and Recovery

All routines below are proposed capabilities. This planning task installs no schedules, services, accounts or credentials.

## Execution modes

| Mode | Trigger | State and authority | Suitable first use |
|---|---|---|---|
| Skill only | Explicit interactive request | Host's authorized tools and project tracker | Analysis or a bounded manual task |
| Offline CLI | Operator supplies captures | Local evidence; no network/model credentials needed | Reproducible audit and schema checks |
| Shadow runner | Qualified scheduler or event | Durable private ledger; read-only bindings | Continuous observation and proposal comparison |
| Native writer handoff | Reviewed candidate under existing mandate | Native writer owns side effect and receipt | Narrow source/metadata change |

The existing observer measures local package/configuration readiness. Preserve that purpose during extraction. Do not present its successful scheduled execution as public crawling, GSC inspection, answer measurement or autonomous specialist execution.

## Three controlled loops

1. **Observation:** daily or event-triggered incremental checks of allowed public targets and available aggregates. Deterministic no-change checks use zero inference. Missing evidence remains unknown.
2. **Asset improvement:** evidence → diagnosis → hypothesis → candidate → proportional review → authorized writer → public verification → measurement window → keep/revert/inconclusive.
3. **Method improvement:** dated source delta and outcome evidence → versioned method/adapter candidate → regression and held-out evaluation → maintainer/authority promotion. Stable instructions never rewrite themselves during a run.

Daily observation is not daily rewriting. Freeze evaluated cohorts during their measurement windows except for incidents; record unavoidable changes and confounders. Security and editorial review should follow the changed surface rather than rerunning every review for every small adjustment.

## Proposed cadence

| Cadence | Work | Noise and cost limit |
|---|---|---|
| Material release/content/price event | Inspect affected pages, offers and locales | Deduplicate event ID; debounce repeated events |
| Daily local readiness | Manifest, instruction and policy integrity | No models; no alert on unchanged state |
| Daily public health, when qualified | Prioritized HTTP/head/robots/sitemap/CTA evidence | Bounded request/byte/time budget; partial coverage reported |
| Weekly | Rotating crawl, demand/content gaps, candidate batch | Reviewer capacity and open findings reused |
| Monthly or appropriate answer window | Fixed answer panel, source delta, cost and outcomes | Comparable cohort; API and consumer UI separate |

The old deployment's local time and timezone remain in its private overlay. The portable example uses UTC. Qualification must test daylight-saving transitions, catch-up policy, overlapping runs, reboot and expired credentials. Do not install a second scheduler when the native one already owns the task.

## Durable state and notifications

Observation records and delivery attempts are distinct. An observation made while notifications are disabled cannot falsely mark its alert as delivered. Each recurrence of a previously resolved condition creates a new occurrence ID linked to the same finding cause. State hashes aid deduplication but do not replace occurrence identity.

Use a transactional outbox or equivalent native mechanism: persist occurrence and queued delivery, attempt delivery, then record the actual receipt. Retry notifications according to their own idempotency semantics. A failure to notify must not delete the evidence or cause the observation to be rerun unnecessarily.

## Conflict and failure runbook

| Condition | Required handling | Work that can continue |
|---|---|---|
| Missing provider credentials | Mark binding unavailable and report exact missing capability | Offline checks and independent sources |
| Safe-read timeout | Bounded retry; preserve last-good timestamp separately | Existing evidence with freshness limits |
| Write timeout or mixed bulk result | Enter reconciling; read current remote state before retry | Unaffected tasks, candidate/report preparation |
| Baseline drift | Rebase the minimal delta; invalidate stale hash-bound review as needed | Nonconflicting targets |
| Lease expires mid-operation | Stop new effects; reconcile already attempted effect | Evidence preservation and incident report |
| Model or budget unavailable | Complete deterministic portion, mark analysis gap | Capture/report with no invented diagnosis |
| Price/catalog unavailable | Suppress unsupported fresh commercial projection | Accepted editorial page and unrelated checks |
| Revocation | Stop affected future effects, revoke credentials if delegated | Audit/retention duties under actual policy |

Leases use fencing or a native equivalent where possible. Providers without CAS still require a fresh read and native serialization; a local lock alone does not exclude dashboard writers. Never claim that this removes every last-write-wins race.

## Retention, observability and rollback

Configure retention by class and purpose before collecting sensitive aggregates. Separate raw captures from minimized observations, proposals, receipts and experiment summaries. Default examples avoid personal data. URL-based service interests can still be sensitive; aggregation alone is not a claim of anonymity.

Observe queue/run age, adapter errors/lag/completeness, actual model usage, budget reservation and reconciliation, repeated proposals, open reviews, unknown writes, verification lag, rollback and denied effects. Runtime usage accounting is cumulative and survives restart.

Rollback changes only the owned delta after reconciling subsequent edits. Preserve native queues, new customer/booking/payment state, revocations, evidence, costs and others' changes. Disable only this deployment's own scheduled job. Exercise recovery in a sandbox before enabling a writer.
