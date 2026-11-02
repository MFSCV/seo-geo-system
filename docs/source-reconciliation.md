# Source Reconciliation and Migration

> Historical integration-design baseline, 2026-11-02. See [current public distribution](current-release.md) for shipped components and adopted publication decisions. Proposed runtime behavior remains unimplemented.

## Baseline inspected

| Source | SHA-256 of supplied ZIP | Actual files |
|---|---|---:|
| `SEO_GEO_Skill_20261102.zip` | `ccc13486d2db1952b066309d1d933399307c209007dd9f66939d44e64d986cfc` | 21 |
| `Agentes_SEO_GEO_AEO_Pack_20261102.zip` | `35dc334d4327dae07c823d217f16b3414633f55628b35deda6a4aa972e827b69` | 33 |

The agent installation report and earlier consolidated plan were also read to interpret the source lineage and intended architecture. Their historical operational statements are not treated as new runtime verification. Original source filenames are retained as identifiers; newly authored descriptions are in English.

The raw source archives are not included in the proposed public package. They contain deployment-specific material and need redistribution review. File-level SHA-256 values and dispositions are recorded in [skill-source-map.csv](../catalog/skill-source-map.csv) and [orchestrator-source-map.csv](../catalog/orchestrator-source-map.csv).

## Mapping completeness

| Inventory | Source count | Target treatment |
|---|---:|---|
| Skill source files | 21 | Every file mapped to a public target, private extraction or replacement decision |
| Agent-package source files | 33 | Every file mapped once; historical verification kept distinct |
| Capability IDs | 144 | CAP-001–CAP-144 preserved, English display labels, role/module ownership and exact original status |
| Roles | 14 | O0 plus S1–S13; no new role namespace required |
| Skill connector entries | 28 | Original CON-01–CON-28 namespace retained |
| Planning connector entries | 25 | Original C01–C25 namespace retained |
| Runtime logical declarations | 10 | Original logical IDs retained as historical source statements |
| Canonical operation families | 76 | Proposed families: 50 read, 26 write; all require implementation/qualification for the unified runtime |

The 63 source connector records yield 190 source-to-operation references. These numbers describe scope and traceability, not enabled integrations. Six operation families retain UI/export evidence with API support unconfirmed. [Connector reconciliation](connector-reconciliation.md) explains the distinctions.

## What was actually checked for this plan

- The existing offline auditor's 33 behavioral tests passed. CLI help and its synthetic example were also checked. This is offline source-tool evidence only.
- The readiness observer's ten existing helper unit tests passed. The effectful observer was not run, no native coordinator was imported, and no schedule was installed.
- All 29 files listed in the agent package manifest match their recorded hashes. This is internal consistency of received bytes, not source authenticity or live installation proof.
- Original source-file hashes were preserved during analysis. File mappings, schemas/examples, internal links and package counts receive separate documentation checks recorded in [verification.json](../verification.json).

## Runtime gaps that change the plan

The observer is not standalone in the archive: it depends on a private root, native policies/store, and a core-verification artifact not supplied here. Its stateful mode acquires a lease, writes checkpoint/evidence state and can submit a native notification. Never execute it just to inspect readiness without understanding those effects.

The legacy candidate core's complete TypeScript code, its 48-test suite, compiled artifacts, native budget broker and coordinator store are absent. Historical source/compiled hash counts and scheduling receipts cannot substitute for inspecting that authoritative checkout. The future implementation must obtain it, check ownership and current instructions, and compare actual interfaces before proposing a Rust bridge or port.

The skill's 144 rows all explicitly describe procedural scope requiring runtime qualification. Fourteen have limited helper/test support; none establishes a completed end-to-end runtime capability. The other 130 are method scope without executable support supplied in the skill.

## Duplicate and conflicting responsibility resolution

| Existing overlap | Unified owner | Migration rule |
|---|---|---|
| Skill procedure and agent common instructions | Canonical method plus role-specific fragments | Remove repeated provider rules; generate self-contained distributions |
| Skill records and agent finding schema | Contract catalog | Versioned bridge preserving IDs, hypotheses and unknowns |
| Three connector inventories | Operation registry and source crosswalk | Preserve source namespaces; qualify each binding separately |
| Source catalog and historical source annex | Dated primary-source registry | Revalidate mutable provider claims; do not inherit historical verification |
| Skill cadence and installed observer | Runtime/scheduler adapter | Local readiness remains local; no second automatic public crawler |
| Native Global routing and generic orchestrator | Authority/coordination adapter | Existing authority stays native; standalone mode uses explicit local authority |
| Repeated reports, backlog and learning templates | S13 and canonical templates | Native tracker remains canonical; reports reference its IDs |
| Fixed model IDs in profiles/config | Private model binding | Public roles use aliases; real invocation evidence records actual provider |
| Clinical/commercial acceptance in project profile | Domain authority extension | Keep private domain semantics; publish only a synthetic profile and generic interface |

## Migration sequence

1. Freeze and hash the source artifacts; obtain the authoritative core and current deployment instructions when implementation starts.
2. Create a private rights/provenance ledger and a clean allowlist for public extraction. Do not carry private history into a new public repository.
3. Preserve source IDs and field semantics through the catalogs and compatibility contracts. Review changed meanings before moving code.
4. Extract the generic method, role fragments, auditor and portable observer parts into an isolated candidate; leave operational files and schedules untouched.
5. Run original tests and new boundary/recovery cases in that candidate. Compare current legacy behavior and new bridge outputs.
6. Start with manual/offline use, then shadow read-only observation on an explicitly qualified site. Reconcile existing schedules and counters before any transition.
7. Change one binding at a time with old-to-new event/receipt references. Confirm no duplicate notifications, competing queues, changed native ownership or reset budget.
8. Retire only owned legacy duplication after a measured acceptance period. Preserve rollback, audit evidence and subsequent human edits.

The [implementation plan](implementation-plan.md) assigns testable outputs. No step in this migration was applied to the operational deployment during this documentation task.
