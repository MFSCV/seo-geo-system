# Unified SEO/GEO System: Integration Design

> Historical integration-design baseline, 2026-11-02. See [current public distribution](current-release.md) for shipped components and adopted publication decisions. Proposed runtime behavior remains unimplemented.

**Version:** 0.1.0-design · **Date:** 2026-11-02 · **Language:** English

**Decision status:** proposed architecture prepared for review. This document authorizes no deployment, recurring job, paid service, external message, or website change.

## 1. Purpose and scope

Unify a procedural SEO/GEO/AEO skill and an O0 orchestrator with thirteen specialist roles into a portable, maintainable system suitable for later open-source publication on GitHub. Preserve the useful existing tools and constraints while making the boundaries between instructions, actual software, external services, and deployment-specific authority explicit.

The public core must support a website, product, service, or other legitimate offer through a project profile. It must not depend on one business, one CMS, a particular Windows machine, a private Global Coordinator, a chat subscription, or a named model being available. Existing deployments can retain those bindings through private adapters.

The objective is qualified discovery and useful transactions, with measured search visibility and accurate answer citations. Top-five coverage is meaningful only for a fixed, documented ranking cohort. An answer's citation order is not a universal ranking. Neither the existing packages nor the proposed system can guarantee permanent positions.

## 2. Current evidence

| Layer | Available evidence | Consequence for integration |
|---|---|---|
| Skill | 21 archived files; method, references, 144 capability rows, 28 connector rows, Python auditor and tests | Reuse the method and auditor; extract private profile; normalize catalogs |
| Agent package | 33 archived files; O0 and S1–S13 profiles, manifest, observer, tests, reports, historical annexes | Preserve role IDs and useful limits; separate deployment bindings |
| Local observer | Source and ten tests are included; installation report describes a scheduled native deployment | Treat it as readiness observation, not public crawling or autonomous inference |
| Legacy core | Historical report refers to a candidate core and source/compiled hashes; full core code is absent | Inspect the authoritative checkout before choosing reuse, bridge, or replacement |
| Connectors | 28 skill entries, 25 planning entries, 10 logical runtime declarations | Reconcile by operation; do not add counts or call them connected services |
| Autonomous execution | Installation report explicitly says the inference binding and permanent executor are not qualified | Future runtime work, not a capability unlocked by combining Markdown |
| Live website and metrics | Historical findings exist; no new live audit is performed for this design | Preserve dated evidence without claiming current deployment or outcomes |

The archives are reproducible source snapshots for this plan. They do not prove the current operational filesystem is unchanged. [Source reconciliation](source-reconciliation.md) records hashes and migration safeguards.

## 3. Architecture choice

| Approach | Benefit | Limitation | Recommendation |
|---|---|---|---|
| Combine all prompts into one skill | Small initial packaging effort | Duplicates policy, confuses scheduling with instructions, loses execution evidence | Retain only as a skill-only distribution mode |
| One modular repository with shared contracts and optional runner/adapters | One reviewable release unit; portable; offline use remains useful; gradual qualification | Needs clear contract ownership and compatibility checks | **Recommended** |
| Separate services and repositories for every specialist | Separate release/scale boundaries | Considerable operating and coordination cost before a working portable baseline | Defer until independent scale or ownership justifies separation |

Use a modular monorepo. Do not deploy fourteen resident model processes. O0 routes bounded tasks to specialists only when their contribution is useful. Deterministic work runs without a model. A simple single-analyst workflow is the benchmark against which extra specialization must earn its cost.

## 4. Component boundaries

| Component | Owns | Does not own |
|---|---|---|
| Skill distribution | Thin entry point, method navigation, task procedure | Credentials, authority, scheduler, ledger, provider execution |
| Shared catalogs | Stable capability, agent, connector-operation, and rule identifiers | Evidence that an operation is implemented or authenticated |
| Contracts | Versioned records, status semantics, examples, compatibility | Business approval or successful live effects |
| Runtime | Durable task state, budgets, routing, deduplication, recovery | Authority to publish merely because a model recommends it |
| Policy boundary | Validate mandate, allowed operations, targets, budgets, review requirements | SEO reasoning or synthetic human acceptance |
| Adapters | Provider-specific reads, writer handoff, receipts, supported errors | Hidden fallback to broader privileges |
| Project profile | Domains, locales, offers, intended index policy, native owners, evaluation cohorts | Secrets embedded in public files |
| Private bindings | Accounts, token references, coordinator protocol, scheduler installation | Public source or default contributor CI configuration |
| Evidence and reports | Minimal findings, provenance, outcomes, proposed improvements | Public disclosure of private production diagnostics |

## 5. Single sources of truth

The proposed canonical sources are `catalog/capabilities.csv`, `catalog/agents.csv`, `catalog/connector-operations.csv`, versioned contracts under `contracts/`, and the reviewed method under `docs/methodology/`. The skill's references and generated agent instruction bundles point to or are generated from these sources. No runtime change may silently edit stable method text.

Each policy rule receives a stable rule ID, owner, evidence link, effective date, review date, and evaluation cases. Provider rules belong to their adapter or dated source registry, rather than being copied into every role profile. Role IDs O0 and S1–S13 remain stable; model aliases such as `analysis` and `review` are resolved by deployment bindings.

Generated skill distributions must remain self-contained: relative references are copied into their package at release time with a source manifest and hashes. A thin skill that points to missing repository-relative files is not an acceptable release. Generation tooling is future work; no such distribution was created here.

## 6. Public and private separation

Publish generic method, role definitions, contract schemas, test fixtures, adapter interfaces, synthetic examples, and authorized original code only after rights review. Keep live profiles, tenant identifiers, private project numbers, local paths, model policy files, account scopes, queues, receipts, commercial budgets, patient/customer information, and raw production evidence outside the public tree.

Keep a private deployment overlay so the existing coordinator, writer, and clinical/commercial owners remain authoritative. Replace private numeric owners with public role names in shared documentation, preserving the mapping privately. A standalone installation uses a local authority adapter; a coordinated installation uses its existing authority. It must not create a competing native tracker or reset usage counters.

Use a clean, reviewed export for the first public repository. Existing private history can contain deleted credentials or sensitive documents. A clean export limits what is transferred; it does not prove that every exported byte is safe or legally redistributable.

## 7. Technology decisions

New portable runtime work is proposed in Rust: small crates for contracts, policy, durable state, engine, and CLI. This is a design choice aligned with the existing engineering direction, not evidence that a Rust runtime exists. Start with a single process and local durable storage; do not require Kubernetes, a cloud queue, or a hosted dashboard.

Retain the existing Python standard-library offline auditor and readiness observer while their behavior is useful and qualified. Bridge their JSON results to the shared contracts. Port only when compatibility, packaging, or measured maintenance cost justifies it. The absent legacy TypeScript core requires inspection before any rewrite decision. CMS and model adapters may use supported SDKs in their appropriate language behind a versioned boundary.

Initial transports are local files/stdin and a CLI. MCP is an optional host integration, followed only if needed by an authenticated HTTP interface. These transports expose the same application operations and policy checks, rather than separate authorities.

## 8. Delivery boundaries

| Milestone | Deliverable | Exit evidence |
|---|---|---|
| D0 | Documentation candidate, mappings, proposed schemas, synthetic examples | Complete mapping; English documentation; schema/example and link checks |
| M1 | Rights-cleared skill and offline tools distribution | Original tests pass; self-contained skill; clean export; no scheduler installation |
| M2 | Portable offline workflow runtime | Restart, deduplication, budget, conflict, and unknown-outcome tests pass |
| M3 | Qualified read-only connectors and shadow diagnosis | Actual per-operation receipts for exact properties; useful findings and measured cost |
| M4 | Native writer handoff for a narrow allowed action | Mandate, review, drift detection, reconciliation, rollback, public verification |
| M5 | Evidence-triggered improvement and method promotion | Comparable outcome window and held-out evaluation; no permission self-escalation |

There is no committed deadline, guaranteed ranking outcome, vendor subscription, or operating budget in this design. The release sequence can stop at a useful offline tool or skill-only release.

## 9. Decisions retained for the owner

The public export now uses `MFSCV/seo-geo-system`, with MIT for the included authored work and MFSCV as initial maintainer. See [current public distribution](current-release.md), [license decision](license-decision.md), and [publication evidence](../verification.json). Runtime deployment, live integrations, operational authority and any future operating budget remain separate decisions.
