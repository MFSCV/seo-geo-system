# Connector inventory reconciliation

> Historical integration-design baseline, 2026-11-02. See [current public distribution](current-release.md) for shipped components and adopted publication decisions. Proposed runtime behavior remains unimplemented.

This is a proposed operation mapping for a future unified, open-source SEO/GEO system. It reconciles three planning inventories without executing connectors, changing their source files, qualifying credentials, implementing adapters or asserting new API support. Every registry operation is `NOT_IMPLEMENTED` and `NEEDS_QUALIFICATION` in the proposed system. A historical declaration that another system already had a component is preserved as source evidence; it does not change those implementation states.

The intended public bundle paths are `catalog/connector-operations.csv` and `catalog/connector-crosswalk.csv`. The registry draft is currently named `connector-operation-registry.csv`. The capability contract belongs in `docs/contracts/connector-capability.md`, with a future machine-readable form at `contracts/connector.schema.json`; neither interface is implemented by this reconciliation.

## Exact accounting

| Source inventory | Source identification | Source records | Crosswalk records |
|---|---|---:|---:|
| Skill connector catalog | Original `CON-01` through `CON-28` | 28 | 28 |
| Agent planning matrix | Original `C01` through `C25` | 25 | 25 |
| Logical runtime declarations | Original item IDs in `connectors.v1.json` | 10 | 10 |
| **Total** | Three separate namespaces | **63** | **63** |

The crosswalk contains **190 source-to-operation references**, covering **76 distinct proposed operations: 50 reads and 26 writes**. These are different counts: 63 inventory records are not 63 installed connectors; 190 references are not 190 independent capabilities or connections; 76 proposed operation contracts are not 76 implemented methods. A runtime item can name an entire component or provider family, and therefore can expand to many candidate operations. Such expansion describes scope to qualify, not confirmed method availability.

The crosswalk retains every original source row ID exactly once in its own inventory namespace. English labels and summaries replace the original non-English prose. Original provider names remain where needed to explain adapter candidates. Project-specific person names, host names, account identifiers and internal numeric owner labels are excluded from the public candidate. Historical evidence is explicitly labeled and is never promoted to authenticated current state.

Validation compared the generated source-ID sets with the three untouched input files, checked unique operation IDs, checked every crosswalk reference and checked that every operation has at least one source reference. These are document consistency checks, not connector, authentication, integration or runtime tests.

## Canonical operation rules

Operation IDs are proposed stable, provider-neutral capability names. Their scope is the unit of authorization and evidence. Provider, product, interface, environment, resource and credentials belong to a separate adapter qualification record. For example, `search.performance.read` can have separately qualified GSC and Bing bindings; neither binding qualifies the other. Renaming or replacing a provider adapter must not rename the stable operation.

Reads and writes are distinct registry rows. `access_mode=read` includes bounded inspections, permitted nontransactional tests and external observations. It does not mean zero cost or permission to send arbitrary data: generated-answer sampling still requires qualified egress, purpose and budget. `access_mode=write` includes local derived artifacts, candidate proposals, control-plane changes, remote mutations, publication, external review requests and external communications. `effect_class` distinguishes these effects so that a local report never grants publication authority.

These IDs are operation families, not invented endpoint names. Where a provider supports single-item and bulk forms within one family, qualification must bind the exact method, batch semantics and item receipts. Where effects differ materially, the registry splits them: redirect create, delete and bulk operations are separate; search reporting is separate from inclusion control; source proposals are separate from release publication. A broad source row never supplies authority for every mapped operation.

A registry record carries:

| Column | Meaning |
|---|---|
| `operation_id` | Proposed stable provider-neutral operation identity |
| `label` | English description of the operation |
| `access_mode` | `read` or `write`; never inherited wholesale from a connector name |
| `effect_class` | Read-only, nontransactional test, external observation, local artifact, candidate artifact, control-plane mutation, remote mutation, publication, external request or communication |
| `field_scope` | Data fields or control fields covered by this operation family |
| `field_owner` | Competent authority for those facts, settings or state; not automatically the SEO operator |
| `role_owner` | Public functional role responsible for proposing or performing the work within an authorized binding |
| `priority` | Proposed planning priority; not an authorization, enabled state or guaranteed delivery order |
| `implementation_state` | `NOT_IMPLEMENTED` throughout this future-system candidate |
| `qualification_state` | `NEEDS_QUALIFICATION` throughout this mapping; details belong to operation-and-environment qualification records |
| `candidate_adapter_families` | Source-supported adapter possibilities, not installed integrations |
| `capability_support` | Preserved contract or availability boundary; not proof of current support |
| `qualification_limits` | Operation-specific constraints and claims that must not be inferred |
| `source_row_refs` | Reverse references to all mapped source records |

Field ownership and role ownership are intentionally separate. A measurement specialist can consume approved conversion aggregates while the operational and finance owners retain authority over their meaning. A technical SEO specialist can diagnose metadata while the native website writer retains the exact write path. Editorial, professional, commercial and privacy approval do not arise from a model or connector being available.

Priorities follow the narrower operation-specific source row where a broad family row also maps to it; otherwise the more urgent applicable source priority is used. A broad P0 SEO-family row therefore does not promote every specifically P1 metadata-pattern operation to P0. Conditional merchant feed work remains `P3`; it is retained rather than silently dropped because it is outside an initial pilot. A high read priority does not authorize a related write. Scheduling and scope decisions remain with the actual project coordinator.

## Boundaries preserved from the sources

| Capability boundary | Canonical treatment |
|---|---|
| GSC Search Analytics versus SERP observations | `search.performance.read` and `serp.observation.read` are distinct; reported average position is not an observed exact consumer SERP. |
| Conversion outcomes versus analytics and service catalog | `conversion.outcomes.read` is a separate minimized aggregate contract; it grants no private booking or finance actions. |
| Merchant feeds | `merchant.feed.read` and `merchant.feed.publish` remain distinct conditional capabilities; product eligibility is not inferred from a service catalog. |
| GSC indexed-state inspection | `search.index-state.read` includes indexed evidence only; no live test or indexing-request API is invented. |
| GSC manual actions and security reports | Separate reads retain an official UI/export route with API unconfirmed. No report endpoint is fabricated. |
| GSC generative report | `search.generative-performance.read` retains API-unconfirmed UI/export status; no clicks, position or exact-prompt fields are added. Overlapping report totals must not be summed. |
| Generative inclusion control | `search.generative-inclusion.read` and `.write` are separate from report reading; control mutation is outside default observation. |
| Bing AI report | `search.ai-performance.read` retains API-unconfirmed official report/export status. Preview, sampling, taxonomy and property availability require qualification. |
| Search-provider submissions and IndexNow | Sitemap submission, provider URL submission and IndexNow notification are distinct operations; accepted receipt is not indexing proof. |
| Raw answer-surface search versus generated answers | `answer.search.read` and `answer.response.sample` are separate; provider APIs and consumer interfaces require separate cohorts and qualification. |
| X search versus xAI answers | `social.public-search.read` remains separate from generated-answer sampling, credentials and costs. |
| Source and control operations | Documentation, evidence, repository, release, audit candidate, report, task, routing, leases and schedule operations remain explicit rather than hidden inside a provider connector. |
| Wix SEO, routes and publication | Site, pattern, item and resolved metadata are separate families; generated sitemap and route registration use the existing writer and publication flow. |
| Browser fallback | Only bounded, permitted, nontransactional evidence is mapped. A broad historical mention of authorized UI writes does not create a generic mutation operation or credential bypass. |

Six operation rows explicitly retain `UI_OR_EXPORT_ONLY_API_UNCONFIRMED`. This support value describes the source inventory's evidence boundary, not a permanent assertion that an API can never exist. If current authoritative documentation later establishes a supported method, a reviewed adapter qualification update must record that evidence. Until then, route the operation through a permitted available UI/export or mark it unavailable. Tool discovery, an installed app and a successful neighboring method are insufficient.

Other support values also remain evidence-limited. `CONTRACT_CANDIDATE_ONLY` means a contract was cited or a capability proposed in the inputs and has not been revalidated here. `PLATFORM_DEPENDENT_UNVERIFIED` means actual infrastructure, binding, interface or eligibility must first be established. Unsupported effects called out in the crosswalk remain excluded: no booking/payment action, fabricated report metric, assumed GSC submission method, false local-business eligibility or private social-data access is made available by this registry.

## Operation and environment qualification proposal

There must be no single overall connector `ready=true` flag. Qualification is scoped to the tuple:

`operation_id + adapter_id/version + provider/product/interface + environment + resource binding + access mode`

A sandbox read does not qualify a production read. A production read does not qualify a write. API and consumer UI samples are separate bindings. An official export can satisfy a read requirement while API support remains unknown. A provider may be unavailable for one property and available for another. Source declarations and implementation state remain separate from all of these facts.

The future qualification record should keep the following independent dimensions:

| Dimension | Proposed record fields and states |
|---|---|
| Identity and scope | `qualification_id`, `operation_id`, `adapter_id`, `adapter_version`, `environment_id`, opaque `resource_alias`, `access_mode`, owner roles |
| Contract support | `support_state`: `unknown`, `documented`, `ui_or_export_only`, `unsupported`; exact product, interface and method where actually supported; contract version, source reference, retrieved and effective dates |
| Implementation | `implementation_state`: `not_implemented`, `candidate`, `implemented`; revision and validation evidence when present. This is not access qualification. |
| Resource binding | `binding_state`: `unbound`, `bound_unverified`, `verified`, `stale`, `revoked`; evidence that the chosen adapter targets the intended resource |
| Authentication and scopes | Separate `read_auth_state` and `write_auth_state`: `not_assessed`, `not_required`, `verified`, `insufficient`, `expired`, `revoked`; secret references only, never credential values |
| Field authority | Accepted `field_scope`, field owner, writer owner and authority reference; unresolved field ownership blocks the dependent mutation only |
| Purpose and data handling | `purpose_state`, permitted dimensions, minimization rules, egress, retention and consent decision reference; approved, rejected, missing or expired as applicable |
| Budget and operation limits | Applicable budget approval, provider quotas, cadence, batch limits, retry policy and observed costs; `not_required` must be explicit when true |
| Read evidence | Per-check result `not_checked`, `passed`, `failed`, `not_applicable`, `stale`; bounded receipt, observed time, data interval, freshness, coverage, watermark and completeness |
| Mutation evidence | Separate mandate, concurrency guard, lease, pre-read, accepted diff, idempotency/reconciliation policy, rollback and item-result checks; each has its own status |
| Execution environment | Interactive or unattended mode; credential renewal, scheduler authority, cancellation, revocation and expiry evidence. An interactive success does not establish unattended operation. |
| Outcome | `observed`, `partial`, `unknown`, `unavailable`, `stale`, `zero_confirmed` or `error`, plus provenance and uncertainty; HTTP or API acceptance is not the domain outcome |

The record should expose the relevant check outcomes and evidence, rather than collapsing them into a misleading connector health score. An authorization decision can be computed for one proposed action from current applicable checks, but must name the exact operation, effect and environment. It expires or is invalidated when the binding, credentials, authority, interface, deployment, contract or material source evidence changes.

For a UI-only report, an empty `api_method` is valid when `support_state=ui_or_export_only` and `interface=official_export` or a permitted official UI. It must never be filled with a guessed endpoint to satisfy a schema. An `unsupported` method is recorded as excluded; lack of a report, lack of data and a real zero are separate outcomes.

Write qualification is stricter only for the actual effect. A local derived report needs the permitted input and artifact destination; it does not need a website-publication mandate. A remote metadata mutation needs the exact writer, field scope, pre-read, accepted diff, conflict controls and recovery evidence. An uncertain mutation response suspends that dependent mutation until state is reconciled; it does not block unrelated reads. Public communication and publication require their own exact mandate rather than inheriting one from a diagnostic task.

The public open-source package should contain contracts, adapters, fixtures and sanitized qualification templates. Actual resource bindings, account or tenant identifiers, private source payloads, secrets, operational logs and customer data belong in private deployment configuration or private evidence storage. Public examples must use explicit placeholders and must not claim that those placeholders are authenticated environments.

## Reconciliation outcome

The two CSVs form a reviewable mapping candidate. They retain the 63 source records, preserve unsupported and UI/export boundaries, distinguish shared operation families from provider bindings, and keep capabilities that appear in only one inventory. No connector was called, no original inventory was modified, and no new code, scheduler, crawler, publisher or credential integration was implemented. Current provider contracts and all environment-specific access remain to be qualified during the implementation phase.
