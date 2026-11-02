# Records and capture contract

## Shared semantics

Use stable IDs, schema version, source revision/hash, observed time or data period/timezone, owner and provenance. Keep unknown, not applicable, real zero, censored/not available and failed collection distinct. Store only the minimum allowed public/aggregate evidence.

Use separate status dimensions; do not force a linear ready flag:
- editorial source/claim reviewed or pending/revoked;
- translation coverage/acceptance;
- commercial price freshness;
- operational availability;
- integrated source revision;
- deployed revision and public verification;
- engine discovery/crawl/index/canonical state;
- measured impressions/citations/conversion.

Public editorial validity does not expire merely because slots or price are temporarily unavailable. A new clinical claim can invalidate dependent translations; price synchronization need not invalidate unrelated clinical review.

## Core records

| Record | Required working fields |
|---|---|
| Project profile | project/site/property/domain, market, platform/deployment, source/live revision, authorities, locales, tracker, mandate, actual connector capabilities |
| Page | pageId/type, URL, service/entity ID, locale/market, source/owner, status dimensions, intended canonical/index policy with reason, actual observed head |
| Intent cluster | primary/secondary terms/questions, page owner, exclusions, demand source/period/geography, confidence |
| Claim | text/field, source/version, competent reviewer, real review date, acceptance hash, dependents, expiry/revocation trigger |
| Commercial projection | source resource/revision, price/currency/inclusions, observedAt/TTL, stale/unknown handling, derived fields |
| Observation | observationId, target, collector/version, time/period/timezone/lag, scope, evidence, observed/unknown/not-applicable and confidence |
| Finding | stable ID, affected surfaces, desired/observed state, cause known/hypothesis, severity/consequence, minimal evidence, reproduction, owner/next action |
| Change | exact target and baseline/hash, complete delta, source/review/authority, side effects, tests/cost, measurement window and rollback |
| Receipt | request/operation ID, target/revision, planned/attempted/applied/verified-live/failed/partial/unknown, per-item results and evidence |
| Experiment | hypothesis, group/control, intervention, baseline/window, primary metric/guardrails/minimum effect, stopping rule, confounders, result |
| Learning | linked observations/experiment, conclusion confidence, negative/inconclusive evidence, proposed method version, evaluation and promotion decision |

Page content may include title/description/H1/summary/sections/FAQ, real reviewer/sources, OG/cards, media rights/alt/dimensions, breadcrumbs and direct calendar. Field necessity is conditional by page; do not force dozens of mandatory values for a minor fix. IDs and commercial data derive from the existing authority.

## Offline HTML capture

The bundled helper accepts JSON:
```json
{
  "document": {
    "url": "https://example.test/service",
    "status": 200,
    "headers": {"Content-Type": "text/html"},
    "html": "<!doctype html><html lang=\"en\"><head><title>Example service</title><meta name=\"description\" content=\"Public service information\"><link rel=\"canonical\" href=\"https://example.test/service\"></head><body><h1>Example service</h1></body></html>",
    "expected": {"indexable": true, "canonical": "https://example.test/service", "locale": "en"}
  }
}
```

Use `documents` for a batch; provide exactly one of `document` or `documents`. The example file provides an actual runnable capture. Headers omitted means unobserved, not an empty verified header set. Missing/failed fetch is unknown.

Run `python3 scripts/audit_snapshot.py --help` for exact options. Output is JSON with schemaVersion, scope `offline-capture-not-live`, documents and summary. Findings carry code/severity/minimal evidence; URL query/fragment are redacted. Exit 0 means no captured error findings, not proof a page is indexed; exit 1 denotes error findings; exit 2 denotes invalid input/invocation. Optional output is create-only.

The helper can flag captured title/description/canonical/robots/locale/hreflang/JSON-LD issues. It cannot establish live access, HTTP-header completeness without capture, semantic truth, clinical adequacy, rich-result eligibility, indexation, ranking, consent or authorization. Do not use its absence of findings as a publication approval.
