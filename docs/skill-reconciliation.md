# Existing SEO/GEO skill reconciliation

> Historical integration-design baseline, 2026-11-02. See [current public distribution](current-release.md) for shipped components and adopted publication decisions. Proposed runtime behavior remains unimplemented.

Documentation draft dated 2026-11-02. This inventory inspects the supplied `seo-geo/` source package and the supplied orchestration role profiles for integration planning. It does not create a skill, implement a public runtime, install an automation, publish a repository or change the original files. No external claims were reverified online during this inspection.

The existing skill is a method with one real offline capture helper. Its catalog describes 144 capabilities and 28 connector scope rows; those counts do not represent implemented runtime functions or qualified adapters. Preserve the useful method, keep the helper's narrow behavior, and connect both to one shared set of records, operation contracts and role definitions.

## Deliverable interpretation

`skill-source-map.csv` covers every one of the 21 supplied source files, including SHA-256, proposed public destination, reuse/adapt/extract-private/replace decision, risk and specific rationale. `catalog/capabilities.csv` covers every existing capability ID, translates display labels to English, preserves the exact existing source status, and proposes one lead owner, supporting owners and documentation/contract/future-module targets. These destinations are a proposed design; the files and modules are not implemented by this inventory.

The capability map is suitable as the source for the planned `catalog/capabilities.csv`. Keep its source status distinct from later implementation or qualification evidence. A historical reference to another project's implementation is not evidence that its code is included in this package or currently operates.

## Observed counts and source shape

| Item | Actual count | Interpretation |
|---|---:|---|
| Supplied skill files | 21 | One `SKILL.md`, one host metadata file, two assets, two Python files and 15 reference files |
| Capability rows | 144 | IDs `CAP-001` through `CAP-144`, unique and contiguous |
| Capability areas | 18 | Exactly eight capability rows per area |
| Distinct capability source-status values | 1 | All 144 rows have the same explicit procedural scope status |
| Connector rows | 28 | IDs `CON-01` through `CON-28`, unique and contiguous |
| Primary-source register IDs | 31 | `S01` through `S31`; public source pointers and dated assertions, not current verification |
| Python behavioral test methods | 33 | One supplied `unittest` test file |
| Runnable offline example captures | 1 | One English synthetic `example.test` document |
| Live connector implementations in this skill | 0 supplied | Documentation recipes and catalog rows do not implement connectors |
| Installed schedules or unattended inference executors in this skill | 0 supplied | Cadence and runner requirements are proposals/contracts |

Every capability source row states exactly:

> Procedural scope catalog; runtime qualification required; not an implemented connector

This status remains verbatim in `source_status_exact`. Fourteen map rows reference limited helper or helper-test support: `CAP-008`, `CAP-027`, `CAP-028`, `CAP-033`, `CAP-037`, `CAP-038`, `CAP-040`, `CAP-041`, `CAP-065`, `CAP-067`, `CAP-083`, `CAP-086`, `CAP-132` and `CAP-134`. None is marked as a completed catalog capability. The other 130 rows have documented method without executable support supplied in this skill.

| Capability area | ID range | Proposed usual lead |
|---|---|---|
| Profile and inventory | CAP-001–CAP-008 | S1 |
| Demand and intent | CAP-009–CAP-016 | S3 |
| Pages and content | CAP-017–CAP-024 | S4 |
| Keywords and metadata | CAP-025–CAP-032 | S4 / S3 |
| HTTP and rendering | CAP-033–CAP-040 | S2 |
| Canonical and discovery | CAP-041–CAP-048 | S2 |
| Migration and redirects | CAP-049–CAP-056 | S2 |
| Links and architecture | CAP-057–CAP-064 | S2 |
| Internationalization and accessibility | CAP-065–CAP-072 | S5 / S8 |
| Media and multimodal | CAP-073–CAP-080 | S8 |
| Entities and structured data | CAP-081–CAP-088 | S6 |
| GEO and bots | CAP-089–CAP-096 | S7 / S2 |
| Organic and AI measurement | CAP-097–CAP-104 | S10 / S7 |
| Performance and experience | CAP-105–CAP-112 | S8 |
| Authority and reputation | CAP-113–CAP-120 | S9 |
| Agents and connectors | CAP-121–CAP-128 | O0 |
| Security and publication | CAP-129–CAP-136 | S11 / S2 / S4 |
| Learning and evolution | CAP-137–CAP-144 | S13 / S10 / S12 / O0 |

The CSV resolves row-specific exceptions. S12 provides independent qualification where needed; it is not the drafter's substitute for human clinical/commercial acceptance or actual release authority. These proposed assignments use the inspected O0 and S1–S13 role definitions rather than inventing new specialist identities.

## Offline helper: actual implementation

`scripts/audit_snapshot.py` is a Python standard-library command. It reads supplied UTF-8 JSON from stdin or `--input PATH`; it performs no network request, crawling, browser interaction, model call or page-script execution. `audit(payload)` itself performs no I/O. No third-party Python dependencies are imported.

The envelope contains exactly one of `document` or `documents`; a batch must be a nonempty list. Each document requires an absolute HTTP(S) URL. Status, headers and HTML may be missing/unknown. Expected indexability, canonical, locale and title are optional assertions supplied by the caller. The helper does not discover the desired policy or validate that the caller's expectation has authority.

The actual CLI is:

```text
usage: audit_snapshot.py [-h] [--input PATH] [--output PATH]
```

| Option | Actual behavior |
|---|---|
| `-h`, `--help` | Prints ordinary argparse help and exits 0 |
| No `--input` | Reads JSON from stdin |
| `--input PATH` | Reads the named input as bytes and decodes UTF-8 |
| `--output PATH` | Exclusively creates a new local JSON report; an existing path causes `output.exists` and exit 2 |
| Successful audit | Always prints the JSON report to stdout, including when an output file is created |
| Input size | Rejects more than 4 MiB with `input.too_large` |

| Exit code | Exact meaning |
|---|---|
| 0 | No captured findings of severity `error`; warnings and unknowns can still be present |
| 1 | At least one captured finding of severity `error` |
| 2 | Invalid invocation, invalid/unreadable/oversized input, existing output or unwritable output |

Invalid invocation is emitted as JSON with `invocation.invalid`. Other handled error codes are `input.invalid`, `input.unreadable`, `input.too_large`, `output.exists` and `output.unwritable`. These exit codes do not establish live reachability, indexation, publication readiness or semantic truth.

Validation rejects credentials in URLs, whitespace/control characters including decoded URL controls, non-HTTP(S) schemes, malformed ports, backslashes and percent characters in hostnames. Status must be an integer from 100 to 599, with booleans rejected. Headers must be an object with string or string-list values. It validates the shape of optional expectations. This is input validation for an offline program; it is not a network SSRF defense, DNS/redirect policy or an authorization boundary for future crawlers.

The parser collects title, description, robots/googlebot, canonical and hreflang from the captured head, the HTML `lang`, and JSON-LD script blocks anywhere in the document. Literal markup in script/style/comment data does not become head metadata. It does not run JavaScript, inspect a hydrated DOM, extract H1/body content, validate `dir`, or prove the capture was initial SSR.

Implemented checks include:

- Missing/non-200 supplied status, missing supplied headers/HTML, and incomplete JSON-LD represented as unknown where applicable.
- Captured title presence and expected normalized title, description presence, canonical presence/duplicates/URL validity/origin/expected identity.
- Generic and bot-specific robots scope, including repeated/list-valued `X-Robots-Tag` fields; unexpected noindex compared with the caller's expectation.
- A warning when a complete supplied capture expected to be non-indexable lacks generic noindex; this explicitly does not verify access control.
- Basic locale-tag pattern and expected locale comparison; hreflang syntax/duplicates, without reciprocal-target checks.
- JSON-LD JSON parsing, rejection of non-standard JSON constants, duplicate identified nodes and conflicting properties for the same `@id`.

Reports use `schemaVersion: "1.0"` and `scope: "offline-capture-not-live"`, with per-document signals/findings and summary counts for `error`, `warning` and `unknown`. This helper schema version is independent of the orchestration package's version.

`offlineIndexability` is one of `blocked`, `unknown` or `not-blocked-by-captured-signals`. Generic captured noindex or a known non-200 status yields `blocked`; bot-only noindex, missing observations or incomplete JSON-LD can yield `unknown`. An absence of captured blockers is not engine index state. The caller must preserve these labels rather than convert them to an `indexed` boolean.

Reports omit raw HTML, title/description text, header values, invalid URL contents, JSON-LD contents and URL query/fragment. Comparison can still use query internally while output redacts it. Paths remain in report URLs, so callers must minimize or exclude sensitive paths before input. Missing headers are unknown; supplying `{}` is a caller assertion of provided headers and is not independent proof of complete collection. There is no retention service, credential store, patient-data classifier or privacy approval implementation.

## Tests present and tests actually run

The supplied `scripts/test_audit_snapshot.py` has 33 behavioral test methods. It starts the helper in subprocesses using synthetic data and temporary files. Coverage includes good captures, entity decoding, robots scope, intentional noindex, missing observations, non-200 status, canonical validity/duplicates/query redaction/port zero, title/locale comparison, hreflang syntax, JSON-LD errors/incomplete blocks/conflicts, script/comment literals, body metadata, missing attribute values, batch exit behavior, input limits/shape, create-only output and invalid invocation.

Some current fixture prose is Portuguese. A public English adaptation should translate that prose while retaining explicit Unicode and HTML-entity coverage. Relocating the test and helper also requires changing the test's `SCRIPT` locator; this inventory proposes that change and does not perform it.

Executed on 2026-11-02 from the supplied skill directory:

| Command | Observed result | What it proves |
|---|---|---|
| `python3 scripts/audit_snapshot.py --help` | Exit 0; the three documented CLI options displayed | Actual current CLI agrees with the description above |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -v` | Exit 0; 33 tests passed | Supplied offline behaviors passed in this environment |
| `python3 scripts/audit_snapshot.py --input assets/snapshot.example.json` | Exit 0; one document; zero errors, warnings or unknowns | The supplied synthetic capture is runnable and produces `not-blocked-by-captured-signals` |

No live HTTP, browser, Wix, GSC, Bing, IndexNow, analytics, CDN, external model, schedule, site build or publication test was run. The method regression scenarios in `references/evaluation.md` are documentation, not an implemented harness or supplied held-out case corpus. Test results do not qualify those integrations or establish clinical adequacy, current search policy or production authorization. Bytecode writing was disabled for discovery; the original sources were not edited.

## Duplicate responsibilities to reconcile

| Responsibility appears in | Reconciliation |
|---|---|
| Skill workflow, agent COMMON and O0 | Keep shared behavior in one methodology workflow; O0 owns bounded dispatch and consolidation; native consumer tracker remains task authority |
| Skill agents/connectors, orchestration connector manifests and operation matrices | Preserve source IDs in a crosswalk; make operation-specific qualifications canonical, with availability/documented/authenticated/read/write/live/unattended separate |
| Skill contracts and agent finding/report templates | Make records and machine schemas canonical contracts; report templates project those fields instead of defining another incompatible record family |
| Skill technical/editorial method and S2–S9 profiles | Method defines checks and limitations; profiles define specialist remit; capability catalog supplies row-level ownership |
| Skill security/autonomy and agent COMMON/S11 | Keep public effect-based safety rules once; actual native policy and task mandate decide access and mutation |
| Skill publication workflow, S12 and native domain writers | Independent review evaluates exact scope; only the qualified native writer changes the product; review is not publication authority |
| Skill offline helper and existing project SEO auditors | Reuse the helper only when it supplies missing capture checks; integrate through records or an optional adapter rather than installing a second crawler or pipeline |
| Skill improvement loop, readiness observer and S13 | Readiness observation, public SEO observation and method learning are different functions; preserve quiet/no-change behavior and avoid duplicate schedules |
| Skill measurement, S7 and S10 | S7 owns actual answer-surface sampling; S10 owns metric/experiment comparability; one versioned panel and one observation record preserve distinctions |
| Skill source register, S1 and S13 | S1 maintains evidence provenance/freshness; S13 proposes documented learning; the register is one authority for source IDs/dates, not new permission |
| Project profiles, public examples and economic plans | Real bindings, budgets and history remain private consumer state; public examples provide a synthetic schema without operational facts |

The skill's A–F autonomy letters classify effects. The orchestration package's N0/N1 labels describe its initial authorized mode. They are not interchangeable scales and do not automatically grant publication, procurement or data access. The proposed contract needs an explicit effect/mode/mandate crosswalk rather than a broad numeric promotion rule.

## Public and private extraction

Do not publish the original project profile, owner-supplied plans or operational configuration. `references/project-drclick.md` contains real site binding, artifact identities, names, service seeds, internal routing/tracker details and historical observations. `references/platform-economics.md` and the end of `references/sources.md` also contain private project provenance, internal allocations and owner cost proposals. Preserve the general requirements through synthetic public templates; keep current values and decisions in a consumer-owned private profile.

Review indirect references throughout `SKILL.md`, Wix examples, catalog labels, connector observed-state fields, measurement pilot wording and source notes. Generalizing a profile file alone does not remove all consumer coupling. Public defaults for actual site/property/account bindings, credentials, authority, budget, service/locale acceptance, analytics state, live deployment and runtime qualifications must be unset/unknown until the consumer supplies evidence.

The source package includes no license file, repository provenance record or asset-rights declaration. The future repository license must be selected by the appropriate rights holder; reuse classification in this draft does not assert permission to redistribute. The icon is marked for replacement because its authorship/license is not documented. Preserve source hashes privately for traceability; do not imply that a hash establishes ownership.

Public source descriptions, host metadata, catalogs and test fixture prose must be English. Exact original filenames, source IDs, code identifiers and quoted status values can remain for traceability. Provider statements and quotas are dated source assertions from the supplied package; current primary sources must be checked before an execution or recommendation depends on them. No external freshness claim is added by this inventory.

## Recommended single sources of truth

1. `catalog/capabilities.csv`: the complete CAP-001–CAP-144 inventory, English labels, source status, lead/supporting roles, proposed targets and evidence-backed implementation state. Documentation and specialist views should reference it; avoid hand-maintaining separate counts.
2. `catalog/connector-operations.csv` owns operation identities and qualification requirements. `catalog/connector-crosswalk.csv` preserves the CON-01–CON-28 source-family identities alongside the other differently granular inventories. No third competing connector catalog is needed. A catalog row is never sufficient to set `implemented` or `qualified`.
3. `docs/contracts/records.md` plus future machine schemas: common record semantics, provenance, status dimensions and receipts. `docs/contracts/offline-capture.md` documents the exact helper contract separately. Preserve unknown/partial/stale/zero/not-applicable/failed rather than merging them.
4. `docs/architecture.md` and one public generic role manifest: O0/S1–S13 identities, dispatch boundaries and relationships. Public profiles describe roles and bounded outputs; private consumer bindings select real executor, model routing, native queue, budget and policy. A profile does not prove an executor ran.
5. `docs/methodology/`: the shared method used by the skill and role profiles. `skills/seo-geo/SKILL.md` is a thin entry point that routes to those canonical documents and does not duplicate their rules.
6. A consumer-owned private profile and native tracker: real project authority, identifiers, current state, acceptance, costs, account bindings and operational history. Public templates are examples; reports and observations are evidence rather than replacement task queues.

For a later implementation, generate or validate derived documentation against these canonical sources, retain provenance and reject dangling IDs. Keep the offline helper optional and independently testable. Qualify runtime integrations one operation at a time, and report only actual read/write/live/unattended receipts. This documentation task supplies the reconciliation design and honest scope inventory; it supplies no new runtime implementation.
