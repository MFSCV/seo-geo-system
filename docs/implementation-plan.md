# Unified SEO/GEO System Implementation Plan

**Goal:** unify the existing method, roles and useful tools through shared contracts and a portable optional runtime, then prepare a rights-cleared open-source release.

**Architecture:** modular monorepo; self-contained skill distribution; deterministic checks before models; durable state and policy outside models; qualified adapters and native writer handoff.

**Proposed stack:** Rust for new runtime, existing Python tools retained, JSON Schema/CSV/Markdown for contracts and documentation. No runtime is implemented by this plan.

**Specification:** [integration design](integration-design.md), [architecture](architecture.md), [record contracts](contracts/records.md).

## Global constraints

All new public documentation is English. Preserve CAP-001–CAP-144 and O0/S1–S13. Do not publish raw private archives/history. Keep authority and cumulative usage in the native system where it exists. Do not invent provider methods, live observations, competent acceptance or successful execution. No model grants itself permissions. Paid incremental budget defaults to zero. Offline tools remain useful without models or credentials. Public observations, index state and outcomes remain distinct.

All task commands below are **future acceptance targets**, not commands available in this documentation package. Each implementation task starts with the named failing behavior tests, implements the smallest useful interface, runs its checks, and ends in a focused reviewed commit. No test names below are claimed to exist or pass today.

## Review focus

The five most important boundary cases are private authority leaking into public configuration; false readiness from catalogs/profiles; unknown remote effects retried as if failed; stale approvals after concurrent edits; and missing metrics reinterpreted as zero. Tasks 1/3, 6/10, 7/13, 8/13 and 4/10 respectively own these cases.

## Phase A: source extraction and an independently useful offline release

### Task 1 — Establish source rights, baseline and clean export

**Files:** create `docs/provenance/rights-ledger.csv`, `release/public-allowlist.txt`, `release/source-manifest.json`; inspect the exact legacy checkout before any edits.

**Consumes:** the two archive hashes and source maps; actual source ownership evidence. **Produces:** candidate source inventory, approved/excluded/unknown rights per file, authoritative checkout revision.

- [ ] Obtain the absent core code, current native instructions and ownership evidence. Preserve historical evidence when unavailable; block only extraction of that component.
- [ ] Make a test fixture containing synthetic private paths/tokens and an unknown-license file. Check the export rejects all three without exposing their values in logs.
- [ ] Implement an allowlisted clean export; keep raw evidence and deployment overlay outside it.
- [ ] Verify export hashes and rights decisions; manually review privacy/branding and all unknown-source material. Commit only reviewed artifacts.

**Exit:** every included file has an explicit origin and redistribution decision; no unknown-rights file is released. Existing operational files and history remain untouched.

### Task 2 — Normalize catalogs and stable identifiers

**Files:** `catalog/{capabilities,agents,connector-operations,connector-crosswalk,rules}.csv`, `tests/contracts/test_catalogs.py`.

**Consumes:** 21/33 source maps, 144 capability rows, 14 roles, 63 connector source rows. **Produces:** validated canonical IDs and source crosswalk; no authentication status upgrade.

- [ ] Add failing cases for lost/duplicated IDs, unknown role owners, dangling operation references, and a catalog row mislabeled as connected.
- [ ] Preserve exact source IDs; translate display text and keep source status separately from implementation state.
- [ ] Check all 76 proposed operation families, 190 source references and six API-unconfirmed UI/export families against the reviewed registry.
- [ ] Run catalog checks and review source-to-target decisions. Commit the catalogs and test evidence.

**Exit:** complete traceability; no misleading aggregate connector count. MVP implementation selects only necessary operations, not all 76.

### Task 3 — Extract canonical method, focused roles and skill packaging

**Files:** `docs/methodology/*.md`, `agents/COMMON.md`, `agents/profiles/{O0,S1..S13}.md`, `skills/seo-geo/SKILL.md`, `tools/package_skill.py`, `tests/contracts/test_skill_package.py`.

**Consumes:** rights-cleared generic method and role text, normalized catalog. **Produces:** canonical method and reproducible self-contained skill bundle with source manifest.

- [ ] Add failing tests for a broken relative reference, private model/tenant default, generated drift, and omission of the unknown/no-change rules.
- [ ] Extract domain-specific facts and authorities into a private overlay. Deduplicate common/provider rules and retain role-specific outputs.
- [ ] Generate required relative references into the distribution; do not depend on a sibling checkout or paid model.
- [ ] Open the packaged skill in an isolated directory, validate every reference and compare regenerated hashes. Commit method and packaging changes together.

**Exit:** skill-only use is documented and operationally honest; no task or daemon is installed by import.

### Task 4 — Reconcile contract schemas and legacy bridges

**Files:** `contracts/{record-envelope,connector,project,work-order,review,receipt}.schema.json`, `crates/seo-geo-contracts/`, `tests/contracts/`.

**Consumes:** design envelope, records, source capture/finding contracts. **Produces:** typed `Observation`, `Finding`, `Proposal`, `Review`, `Receipt`, `Experiment` and compatibility validation.

- [ ] Add failing cases for unknown versus observed zero, withheld data, inconsistent periods, unsupported major version and invalid cross-project reference.
- [ ] Implement schema/type validation plus explicit bridges retaining original IDs and source versions.
- [ ] Add semantic checks for hash-bound reviews and source/claim references; do not confuse schema validity with authorization.
- [ ] Validate positive and negative fixtures and document migration reports. Commit schemas, types and tests together.

**Exit:** no silent loss or fabricated value across legacy and new records.

### Task 5 — Preserve and package the offline auditor

**Files:** `tools/offline-capture/audit_snapshot.py`, `tests/offline-capture/test_audit_snapshot.py`, `examples/offline-capture/snapshot.example.json`, bridge module in `crates/seo-geo-contracts/`.

**Consumes:** unchanged rights-cleared Python source and shared envelope. **Produces:** packaged offline audit with compatible JSON payload and exit codes 0/1/2.

- [ ] Port the 33 original behavior tests to the extraction without changing their meaning; add a bridge assertion for `offline-capture-not-live`.
- [ ] Preserve stdin/file input, exactly-one envelope rule, redaction and create-only output.
- [ ] Run the original cases, CLI help and positive/error/invalid synthetic captures in the isolated package.
- [ ] Verify no network/model/browser side effects. Commit the usable offline package and limitations.

**Exit:** a useful M1 distribution is possible even if runtime work stops here.

## Phase B: portable, offline execution and shadow analysis

### Task 6 — Implement trusted policy and budget boundary

**Files:** `crates/seo-geo-policy/src/{mandate,budget,target,decision}.rs`, `tests/policy/`.

**Consumes:** work order and private authority/model bindings. **Produces:** `authorize(request, context) -> Decision`; `reserve_cost`, `settle_cost`, and cumulative accounting through the state interface.

- [ ] Add failing tests for a model requesting broader authority, wrong project, zero paid budget, restart-counter reset, and a source page instructing a new action.
- [ ] Enforce exact operation/target/field scope, task ceilings and existing mandate without unnecessary repeated prompts.
- [ ] Reserve before inference/effect; reconcile actual usage and retain unknown costs conservatively.
- [ ] Run deny/allow and restart cases. Commit policy and evidence.

**Exit:** runtime policy, rather than prompt wording, controls effects and cost.

### Task 7 — Durable workflow, outbox and recovery

**Files:** `crates/seo-geo-state/src/{store,outbox,lease,migration}.rs`, `crates/seo-geo-engine/src/workflow.rs`, `tests/recovery/`.

**Consumes:** contract records and authority adapter interface. **Produces:** `enqueue`, `claim`, `checkpoint`, `record_attempt`, `reconcile`, `deliver_outbox` with durable IDs.

- [ ] Add failing crash/restart cases, duplicate/delayed/reordered events, lease expiry, observation-without-send followed by send, and reappearance of a resolved state.
- [ ] Implement transactional local state and native-authority references; no competing authoritative tracker.
- [ ] Keep write outcomes unknown after timeout until current state is reconciled; never assert exactly-once effects.
- [ ] Run fault-injection cases including partial bulk results. Commit state/migration and recovery documentation.

**Exit:** restarts do not reset budget, lose occurrences, duplicate effects or falsely record delivery.

### Task 8 — Bounded routing and independent review

**Files:** `crates/seo-geo-engine/src/{dispatch,packet,review}.rs`, `adapters/model/`, `tests/evaluation/dispatch/`.

**Consumes:** work order, evidence, role catalog, budget decisions. **Produces:** immutable review packet, role output, actual invocation receipt and cause-based consolidation.

- [ ] Add tests for deterministic no-change with zero inference, depth/pass/call limits, unavailable model, false external attribution, own-proposal review and stale proposal hash.
- [ ] Route only useful specialists; resolve private `analysis`/`review` aliases without changing roles.
- [ ] Record actual provider/interface and isolate first reviewer reports from earlier conclusions.
- [ ] Compare with a simple analyst baseline on held-out fixtures. Commit supported routing only after its benefit and cost are understood.

**Exit:** bounded useful analysis with explicit partial/unknown results; no mandatory fourteen-process deployment.

### Task 9 — Portable observer and scheduler/coordination bridges

**Files:** `tools/readiness-observer/observe.py`, `adapters/{coordination,scheduler}/`, `tests/recovery/test_observer_portability.py`, `docs/runtime/observer.md`.

**Consumes:** source observer, state/outbox, native authority protocol. **Produces:** pure `inspect(root, manifest)` result and explicitly effectful `observe(context)` path.

- [ ] Preserve the ten original helper cases; add effectful paths with fake store/budget/notification bindings.
- [ ] Remove hardcoded roots and separate missing evidence from corruption. Test with no private native installation present.
- [ ] Test DST/missed-run/restart/overlap and install/remove only an explicitly owned scheduler job in a sandbox.
- [ ] Verify unchanged state is quiet and returning incidents get a new occurrence. Commit the portable observer and qualification runbook.

**Exit:** local readiness is portable and correctly labeled; no public crawl or inference is implied.

## Phase C: qualified observation and useful diagnosis

### Task 10 — Public capture and first-party read bindings

**Files:** `adapters/{http,gsc,bing,wix}/`, `contracts/connector.schema.json`, `tests/adapters/`, `docs/adapters/`.

**Consumes:** registry operation IDs, target policy and current provider contracts. **Produces:** normalized observations and per-operation/environment qualification receipts.

- [ ] Start with public capture and the needed search-performance/index-inspection/catalog reads; keep UI-only reports on explicit export paths.
- [ ] Add redirects/private-address tests, partial pagination, quota/backoff, token expiration, data lag, withheld data and wrong-property cases.
- [ ] Qualify the real intended account/property using minimal authorized calls outside fork CI; no credentials in fixtures.
- [ ] Compare provider response, captured HTML and intended state without collapsing their meanings. Commit each adapter independently.

**Exit:** every enabled read has current operation-specific evidence. Missing provider support remains unavailable rather than fabricated.

### Task 11 — Shadow findings, content/technical proposals and reports

**Files:** `crates/seo-geo-engine/src/{inventory,technical,intent,content,localization,schema,experience}/`, `templates/`, `tests/evaluation/proposals/`.

**Consumes:** accepted sources, captures, intent and offer identity. **Produces:** evidence-linked findings and minimal proposals, with no external writes.

- [ ] Add fixtures for unintended noindex, stale price, accepted editorial content with catalog outage, locale gaps, wrong calendar target and mismatched redirect intent.
- [ ] Preserve field ownership, competent acceptance and the existing CMS metadata/sitemap writer.
- [ ] Produce draft report/audit/improvement outputs and compare with competent review; track false positives and review burden.
- [ ] Commit only supported diagnosis; document unresolved causes and unsupported surfaces.

**Exit:** useful actionable proposals without degrading accepted content or conversion paths.

### Task 12 — Fixed cohorts, experiments and method promotion

**Files:** `crates/seo-geo-engine/src/{measurement,geo,learning}/`, `catalog/rules.csv`, `tests/evaluation/holdout/`.

**Consumes:** fixed query/answer cohorts and completed observation windows. **Produces:** denominator-complete measurements, experiment decisions and versioned rule proposals.

- [ ] Test unknown cells, zero, API-versus-consumer separation, changing denominators, negative/inconclusive results and unsupported provider claims.
- [ ] Record model/interface/context, lag, sampling and confounders; do not interpret citation order as rank.
- [ ] Evaluate method candidates against regressions and held-out cases, separately from permission policy.
- [ ] Commit promoted changes through ordinary review, retaining rejected outcomes.

**Exit:** recursive improvement is measured and reviewed rather than uncontrolled self-editing.

## Phase D: narrow effectful integration and publication

### Task 13 — Native writer handoff, reconciliation and live verification

**Files:** `adapters/writer/`, `crates/seo-geo-engine/src/{handoff,verification}.rs`, `tests/recovery/writer/`, `docs/adapters/writer.md`.

**Consumes:** hash-bound reviewed proposal, current mandate, qualified writer and fresh baseline. **Produces:** applied/partial/unknown/refused receipt and separate public verification.

- [ ] Test baseline drift, expired lease, stale review, mixed bulk results, timeout-after-apply and concurrent dashboard edits.
- [ ] Implement the smallest allowlisted action through the native writer; use provider idempotency/CAS only when actually supported.
- [ ] Exercise rollback of only the owned delta. Verify local build, managed/platform build and public output as distinct evidence.
- [ ] Confirm calendar/locale/accessibility behavior without a booking, hold, charge or notification. Commit narrow support and limits.

**Exit:** one qualified N2 path; no generalized autonomous publication.

### Task 14 — Release, community and contribution controls

**Files:** root community documents, `LICENSE` only after rights decision, `THIRD_PARTY_NOTICES.md`, `.github/`, release manifest and future SBOM/provenance artifacts.

**Consumes:** ready source candidate, rights ledger, named maintainers, staffed security route and tested release revision. **Produces:** public release candidate with accurate scope and support status.

- [ ] Complete the [publication checklist](publication-checklist.md) for the actual release scope; mark runtime items not applicable for docs-only releases.
- [ ] Review untrusted-PR isolation, least permissions, action/dependency pins, secret/PII scans and manual export review. Do not claim hosted CI is offline by default.
- [ ] Select license and notices through the actual rights holder; configure repository protections and private vulnerability reporting before opening contributions.
- [ ] Produce a reviewable export and release notes. Publish only after the explicit final publication mandate, then verify actual repository/release visibility and content.

**Exit:** an honestly described, licensed, maintainable public release. No ranking gain is a release gate.

## Planning handoff

The documentation and mappings are complete candidates for review. The tasks above remain unchecked because this request covered planning and documentation. The next concrete implementation step is Task 1, followed by the independently useful M1 offline/skill extraction; portable runtime and connected operation remain separate acceptance milestones.
