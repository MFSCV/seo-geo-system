# Shared Record Contracts

The existing skill uses descriptive records, the agent package includes a finding schema, and the observer has its own local state. The target is one versioned vocabulary with compatibility bridges, not immediate replacement of every existing record.

## Identity and provenance

Every persisted record includes `schemaVersion`, `recordType`, stable `id`, `projectId`, `createdAt`, `producer`, and `sourceRefs`. A source reference names a source type, opaque reference, observed time or data period, and a content/revision hash when available. Missing hashes are recorded as unavailable with a reason, never invented.

Times use RFC 3339 UTC timestamps. Data periods also carry the reporting timezone, start/end boundary semantics, source lag and completeness. Scheduling uses an IANA timezone and a separate local time; do not infer it from the execution host.

IDs are scoped by project. Public examples use synthetic IDs. Runtime evidence belongs in a private workspace by default, with export classification recorded. URL query/fragment and sensitive path segments must be minimized before logging, external review, or public export.

## Core objects

| Record | Required domain fields | Important invariant |
|---|---|---|
| ProjectProfile | public origins, locales/markets, offer types, native authority/writer, tracker reference, mandate reference | No embedded tokens; no automatic authority inferred from a profile |
| Page | page ID, offer/entity ID if applicable, locale, URL, intended canonical/index policy and reason, observed state references | Intended and observed state are separate |
| Claim | field/text, source revision, owner/reviewer, acceptance hash, dependents, review/revocation rule | A model cannot invent competent human acceptance |
| CommercialProjection | authoritative resource ID/revision, price/currency/inclusions, observedAt, freshness rule | Freshness does not establish editorial validity |
| Observation | target, collector/version, outcome, evidence reference, coverage and uncertainty | Failed collection is not zero or proof of absence |
| Finding | code, affected target, observed vs intended state, cause/hypothesis, severity, confidence, minimal reproduction, owner | Deduplicate by cause and affected scope, preserve occurrence history |
| Proposal | baseline revision/hash, typed patch or handoff, source/claim links, expected effect, side effects, checks, rollback, measurement window | Patch scope must match current mandate and actual writer ownership |
| Review | proposal hash, reviewer identity/competence, independence disclosure, scope, verdict/reasons | A review of one hash does not approve a changed proposal |
| Receipt | operation/request IDs, target, baseline/result revisions, outcome, per-item results, evidence | Accepted/attempted/applied/publicly-verified are distinct |
| Experiment | fixed cohort, hypothesis, baseline/window, metric denominator, guardrails, decision rule, confounders | Do not change denominator to make a result look positive |
| Learning | observation/experiment links, conclusion/uncertainty, proposed rule/method delta, evaluations, promotion decision | No direct self-modification or privilege increase |

## Project profile

Stable project identity, domains/properties, market, platform, locales, tracker and authority references define context. Credential material and private deployment values stay outside the public record. The capability map uses this section as its `project-profile` target.

## Page

Preserve page/offer/entity identity and locale alongside intended policy, source acceptance, commercial freshness, delivery revisions and engine observations. These are independent dimensions rather than one ready flag.

## Intent cluster

`IntentCluster` records primary and secondary terms/questions, language/market, inclusion/exclusion intent, target page owner, evidence source/period, confidence and known overlap. Demand evidence does not authorize a claim or publication. This is a proposed record described here; its machine schema is future Task 4 work.

## Claim

Record the exact field or text, authoritative source revision, actual competent reviewer, acceptance hash and dependent locales/pages. Track revocation or material source changes; never invent approval dates.

## Observation

Link the collector/version and target to bounded evidence, coverage and time/period. Distinguish every outcome described below. The design schema includes a representative Observation payload.

## Change

`Change` is the legacy vocabulary's compatibility alias for the target `Proposal` record, not a second write authority. Preserve historical change IDs while bridging them to a proposal with an immutable baseline, typed delta, checks, review, writer handoff and rollback. The `change` fragment remains stable for existing capability mappings.

## Learning

Preserve the linked experiment/observation evidence, negative/inconclusive outcomes, confidence, candidate method/rule revision and independent promotion decision. Record the next validation window. A learning record cannot update its own permissions or approve a deployment.

## Observation outcomes

Use `observed`, `unknown`, `not-applicable`, `withheld`, or `collection-failed`. A numeric zero belongs only to a successful observed measurement with a valid denominator. Unknown, withheld and failed records cannot include a fabricated measurement value. `not-applicable` requires a reason; it is not a substitute for a connector error.

For paginated or sampled sources store coverage, filters, returned count, pagination termination, watermark and known limitations. Exhausting a page loop does not establish full underlying coverage where the provider exposes only top rows.

## Operation contract

Proposed language-neutral operations:

| Operation | Input | Result |
|---|---|---|
| `observe` | scoped work order, qualified operation binding, collection limits | Observation batch and receipt |
| `diagnose` | bounded evidence packet and method/catalog versions | Findings with causal confidence |
| `propose` | finding IDs, authoritative sources, current baseline | Proposal; no remote effect |
| `review` | immutable proposal packet, reviewer assignment | Hash-bound review |
| `handoff` | reviewed proposal, mandate, writer binding, current revision | Writer receipt or explicit refusal |
| `reconcile` | unknown/partial receipt and current provider state | Resolved receipt or continued unknown |
| `verify` | expected deployed revision and public assertions | Public observations; never engine-state inference |
| `evaluate` | experiment definition and completed window | Keep/revert/inconclusive decision |

These signatures describe future interfaces; no executable SDK is delivered. [record-envelope.schema.json](../../contracts/record-envelope.schema.json) is a design schema for the common envelope and representative Observation, Finding, Proposal, Review and Receipt payloads. Other record kinds, full provider payloads and cross-record semantic validation are future Task 4 work. Structural validation does not imply runtime enforcement.

## Compatibility and integrity

The legacy finding schema retains a bridge with the original finding code and source schema version. Do not rename historical IDs in place. A bridge must preserve severity, hypothesis status, evidence limits, and unknown values. Unsupported fields survive in a documented extension object or are rejected with a migration report; they must not disappear silently.

Review packets use an immutable content hash and list included files/evidence. External reports declare actual provider/model/interface, date, packet hash, executed checks and unknowns. Internal parallel roles are not attributed to Claude, Gemini or Copilot without an actual call and returned artifact from that provider.

Contract validity is only structural. Runtime policy still checks authority, cross-project references, reviewer competence, revision drift, and whether evidence really supports the conclusion.
