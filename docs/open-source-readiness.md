# Open-source readiness

This document describes the public source export and the separate requirements for future executable or connected releases. Publication was explicitly authorized by the project owner on 2026-11-02. The candidate repository is [MFSCV/seo-geo-system](https://github.com/MFSCV/seo-geo-system).

## Current distribution

The export contains English documentation, catalogs, synthetic records, reusable skill text, local source tools, agent specifications, and templates. [README](../README.md) and component documentation define the implemented scope. The autonomous executor, authenticated integrations, and continuous production publishing remain future work.

Original included materials use [MIT](../LICENSE). [License and provenance](license-decision.md) records scope and exclusions. A clean export is used instead of publishing private project history. Credentials, local machine/user paths, account/property identifiers, coordinator databases/queues, customer records, raw production captures, private archives, and third-party skill source are outside the intended public tree.

Repository publication, remote visibility, tests, and enabled GitHub settings must be verified against the actual candidate revision. Documentation does not by itself prove those operations occurred. See the [publication checklist](publication-checklist.md) and any generated verification record for observed results.

## Practical release gates

| Stage | Evidence required |
|---|---|
| Public source preview | Owner mandate, license/notices, clean manifest, privacy/secret review, English onboarding, honest capability status, component checks, and public visibility verification |
| Installable local software | Reproducible installation, meaningful behavior/denial tests, supported toolchain, dependency/license inventory, release checksums, migration and failure behavior |
| Connected runtime | Qualified operation-level adapters, scoped/revocable identities, controlled egress, budget enforcement, durable state, wrong-target/unknown-outcome recovery, and deployment verification |
| Production publishing | Operator mandate, revision checks, native writer ownership, review and content acceptance, rollback, and verification of actual delivery |

Do not require runtime controls for a component that does not implement that runtime. Do not advertise future controls as already enforced. The security/effectiveness tradeoff must name concrete risks and legitimate workflow costs.

## Repository operation

[MFSCV](https://github.com/MFSCV) is the initial single maintainer. [Governance](../GOVERNANCE.md), [contributing](../CONTRIBUTING.md), [conduct](../CODE_OF_CONDUCT.md), and [security](../SECURITY.md) describe current best-effort processes. Private reporting, branch protection, required checks, and release settings are actual GitHub configuration and must be reported according to what is enabled. No independent reviewer, backup maintainer, or staffed SLA is invented.

Use public issues and pull requests for non-sensitive contributions. Do not execute untrusted contributions with production secrets or privileged runners. Any future CI should minimize permissions, pin reviewed actions, use hosted isolated runners for forks, and avoid unsafe interpolation or `pull_request_target` execution of untrusted source.

Future dependencies need explicit manifests and appropriate lockfiles, provenance and license review, meaningful tests, and an accurate software inventory. A standard-library local tool does not justify inventing an empty runtime SBOM. A future runtime release may need an SBOM and attestations proportionate to its real distribution.

## Continued maintenance

Recheck dated primary sources when provider rules change, evaluate method changes before promotion, retain negative/inconclusive results, retire unsupported adapters, and disclose gaps. No release certifies ranking outcomes, regulatory compliance, universal agent compatibility, or vulnerability absence.

The deeper runtime requirements are preserved in [security and effectiveness](security-and-effectiveness.md), [operations](runtime/operations.md), and the [implementation plan](implementation-plan.md).
