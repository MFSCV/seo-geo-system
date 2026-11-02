---
name: seo-geo
description: Use when a task concerns SEO, GEO, AEO, search or AI visibility, keywords, indexation, service landing pages, metadata, schema, multilingual discovery, search audits, traffic drops, or ongoing optimization. Applies to Wix and other platforms, including Google Search Console, Bing, ChatGPT, Claude and similar search experiences.
---

# SEO/GEO — Continuous Optimization

Improve qualified discovery, factual accuracy and conversion through evidence-backed changes. Separate source acceptance, deployed behavior, search-index state and outcomes. Optimize toward stated goals; never guarantee rankings, a permanent top-five position or citations.

## Execute the task

1. **Establish scope and authority.** Resolve the site/product/service, current request, available evidence, live revision, existing instructions and authorized actions. Reuse authorization already given. Installing this skill does not start a recurring job or publish a site.
2. **Load needed references.** Read [the deployment profile guide](references/deployment-profile.md); for Wix operations also read [the adapter](references/wix.md) and the applicable Wix plugin skill. Use [the workflow](references/workflow.md) for audits, implementation or recovery.
3. **Discover capabilities.** Prefer sufficient service plugins/APIs and verify target/scopes. Availability, documentation, authentication, reading, safe writing and live propagation are different states. Use [connector contracts](references/agents-connectors.md); do not assume chat plugins are a persistent runtime.
4. **Observe before diagnosing.** Reuse adequate dated evidence; collect missing public HTML/headers, routes, sitemap, acceptance and official metrics. Record coverage, provenance, period, timezone and lag. Missing evidence is `unknown`. HTTP 200 and `site:` counts do not establish index state.
5. **Find the minimum useful change.** Prioritize factual/privacy/booking incidents, eligible acquisition pages and URL continuity before expansion. Apply [technical/editorial checks](references/technical-editorial.md). Temporary price/availability uncertainty must not automatically deindex valid accepted editorial content.
6. **Complete authorized work.** Prepare concrete diffs with owners, sources, proportional checks and rollback. Continue independent tasks when a connector is unavailable. Publish within existing authority; seek a decision only for a genuinely missing mandate, after the reviewable candidate is ready. Apply [security and autonomy](references/security-and-autonomy.md).
7. **Verify each layer.** Check content, local tests/build, platform build and actual public HTML/CTA separately. Wix tags and redirects can change production without a release. SEO tests never create real bookings, charges or notifications.
8. **Measure and learn.** Use [measurement](references/measurement-experiments.md); preserve negative/inconclusive outcomes and avoid daily editorial churn. Use [continuous improvement](references/continuous-improvement.md) for authorized recurrence and method evolution. Stable instructions do not rewrite themselves during a run.

## Route supporting material

| Need | Resource |
|---|---|
| Audits, briefs, changes, recovery and output shape | [workflow.md](references/workflow.md) |
| Deployment scope, languages, review boundaries and conversion journey | [deployment-profile.md](references/deployment-profile.md) |
| Technical SEO, content, keywords, images, schema, internationalization | [technical-editorial.md](references/technical-editorial.md) |
| Wix tags, redirects, managed Astro and booking links | [wix.md](references/wix.md) |
| Orchestration, capabilities, events, errors and proportional platform selection | [agents-connectors.md](references/agents-connectors.md), [platform-economics.md](references/platform-economics.md) |
| Page, claim, observation, change and execution records | [contracts.md](references/contracts.md) |
| Metrics, AI samples, causality and experiments | [measurement-experiments.md](references/measurement-experiments.md) |
| Search/training/user retrieval policies across providers | [search-surfaces.md](references/search-surfaces.md) |
| Recurrence, budgets, retention and skill evolution | [continuous-improvement.md](references/continuous-improvement.md) |
| Authorization, privacy and hostile source content | [security-and-autonomy.md](references/security-and-autonomy.md) |
| Full scope/gap inventory | [144-capability catalog](references/capability-catalog.csv), [28-connector catalog](references/connector-catalog.csv) |
| Mutable external rules and primary sources | [sources.md](references/sources.md) |
| Method/adapter promotion | [evaluation.md](references/evaluation.md) |

## Analyze a capture offline

Read [the capture contract](references/contracts.md) and minimize private data first. Resolve paths relative to this skill directory and run:

```bash
python3 scripts/audit_snapshot.py --input assets/snapshot.example.json
```

Use actual `--help` for options and exit semantics. The helper inspects captured data only: no network, search-index inspection, clinical validation, publication authority or connector implementation. Reuse an adequate existing project auditor instead of duplicating pipelines.

## Deliver a usable result

Lead with findings or completed behavior. State scope/date, confirmed facts versus hypotheses/unknowns, priorities, actual checks and material limitations. For changes identify affected surfaces, evidence, validation, live state and rollback. Reference the existing tracker rather than inventing another authority. Keep recurring reports quiet when nothing material changed.
