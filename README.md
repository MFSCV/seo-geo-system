# SEO/GEO System

An open method, reusable AI skill, and agent specifications for improving search discovery, answer visibility, factual accuracy, and conversion.

**Initial public-source candidate · 2026-11-02 · [MIT License](LICENSE)**

SEO means search engine optimization; GEO means generative engine optimization; AEO means answer engine optimization. This project brings these practices into one evidence-based workflow, with an orchestrator (O0), thirteen specialist roles (S1–S13), shared records, review criteria, and controlled improvement cycles.

The goal is useful, measurable discovery across search engines and AI assistants. There is no guarantee of permanent top-five rankings, citations, or a universal position in AI answers.

## What is available

| Component | Current scope |
|---|---|
| [SEO/GEO skill](skills/seo-geo/SKILL.md) | Reusable instructions, references, capability inventory, and an offline captured-HTML auditor |
| [Agent definitions](agents/README.md) | O0 and S1–S13 roles, shared instructions, and portable deployment guidance |
| [Local package inspector](tools/observer/README.md) | Validates local role/configuration files and optional expected hashes; no scheduler, queue, notifications, or network |
| [Architecture and integration design](docs/integration-design.md) | Shared method, records, execution boundaries, migration, and a fourteen-task implementation roadmap |
| [Capability catalog](catalog/capabilities.csv) | 144 scope capabilities with stable IDs and assigned roles |
| [Connector operations](catalog/connector-operations.csv) | 76 proposed operation families reconciled from 63 source entries; these are **not 76 implemented integrations** |
| [Report and audit templates](templates/REPORT.md) | Findings, improvement proposals, independent review, evidence, and decision records |
| [Synthetic examples](examples/deployment.example.json) | Deployment and record examples without production credentials or customer data |

A portable autonomous executor, authenticated Google/Bing/AI integrations, and a continuous publishing system are **future work**. Installing the skill or reading an agent profile does not start a daemon, activate a connector, authorize publication, or schedule a job. Source mappings describe both the original baseline and planned destinations; they are not a claim that every target exists today.

## Try the offline auditor

Use Python 3.11 or newer for the repository checks. The auditor uses the Python standard library and does not need API credentials or network access:

```bash
git clone https://github.com/MFSCV/seo-geo-system.git
cd seo-geo-system
python3 skills/seo-geo/scripts/audit_snapshot.py --help
python3 skills/seo-geo/scripts/audit_snapshot.py --input skills/seo-geo/assets/snapshot.example.json
python3 -m unittest discover -s skills/seo-geo/scripts -p 'test_*.py'
python3 tools/observer/observe.py
python3 -m unittest discover -s tools/observer -p 'test_*.py'
```

The example is synthetic and may deliberately contain audit findings. Follow the auditor's documented exit semantics. Captured HTML cannot establish current live delivery, Google's selected canonical, index state, ranking, clinical correctness, or publication authority. Supply minimized captures from sites you are authorized to inspect.

To use the skill in an assistant, import or copy `skills/seo-geo` using that assistant's supported skill mechanism, then read its `SKILL.md`. There is no provider-independent skill installer in this repository. For agents, start with [agents/README.md](agents/README.md); model names in an example do not prove model execution.

## How the method works

1. Establish the target, authority, baseline, and measurable cohort.
2. Observe published pages, accepted content, routes, and available first-party metrics; record missing evidence as unknown.
3. Diagnose specific causes and choose the smallest useful change.
4. Review factual claims, security, accessibility, conversion, cost, and rollback together.
5. Verify source, build, platform delivery, index state, and outcomes separately.
6. Evaluate changes over an appropriate window and preserve negative or inconclusive results.

Daily observation does not imply daily rewriting. Method updates require separate review and evaluation; agents must not expand their own permissions or treat retrieved content as instructions.

## Read the documentation

| Question | Start here |
|---|---|
| What is the proposed unified architecture? | [Architecture](docs/architecture.md), [integration design](docs/integration-design.md) |
| How are existing assets mapped? | [Source reconciliation](docs/source-reconciliation.md), [skill map](catalog/skill-source-map.csv), [agent map](catalog/orchestrator-source-map.csv) |
| How do specialists coordinate? | [Agent catalog](catalog/agents.csv), [dispatch and review](docs/runtime/dispatch-and-review.md) |
| How do tools earn permission to act? | [Connector contracts](docs/contracts/connector-capability.md), [configuration](docs/configuration.md) |
| What does continuous operation require? | [Operations](docs/runtime/operations.md), [source gaps](docs/runtime/source-gap-analysis.md) |
| How are effectiveness and safety balanced? | [Security and effectiveness](docs/security-and-effectiveness.md), [measurement](docs/measurement-and-learning.md) |
| What remains to implement? | [Implementation plan](docs/implementation-plan.md), [acceptance scenarios](docs/acceptance-scenarios.md) |
| What supports the recommendations? | [Source register](docs/sources.md), [requirements traceability](catalog/requirements-traceability.csv) |
| What was verified for this source preview? | [Current release](docs/current-release.md) |
| How is the public export governed? | [Readiness](docs/open-source-readiness.md), [publication checklist](docs/publication-checklist.md), [license and provenance](docs/license-decision.md) |

Design documents retain their original planning language where they specify future runtime behavior. This README describes the distribution available now. Platform rules change: use dated primary sources and recheck them before deployment.

## Contribute and reuse

All original code, documentation, templates, examples, and included original assets are available under [MIT](LICENSE). You may use, modify, redistribute, and build commercial or non-commercial derivatives under its terms. Linked provider documentation, third-party services, datasets, and trademarks keep their own rights and terms. No paid account is required to read or download this repository; connected services may have their own charges.

Use [GitHub issues](https://github.com/MFSCV/seo-geo-system/issues) for ordinary bugs and proposals, and pull requests for changes. Read [CONTRIBUTING.md](CONTRIBUTING.md), [GOVERNANCE.md](GOVERNANCE.md), and [SECURITY.md](SECURITY.md). The initial maintainer is [MFSCV](https://github.com/MFSCV); no response-time or production-support commitment is promised.
