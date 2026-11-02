# Agents and connectors

## Qualify each operation

Progress independently through catalog availability → documentation → authentication → read qualification → write qualification → propagation → recurring operation. Capture provider/tool version, site/property, identity/scopes, deployment mode, supported methods, pagination, quota/cost, freshness/lag/timezone, side effects, revision/idempotency and errors. A successful read proves neither writing nor future unattended access.

Prefer sufficient service plugins/APIs. Use only permitted fallbacks when an operation is missing; a UI widget is not an API and a chat session is not persistent runner credentials. Never ask users to install a connector already capable of the authorized work. Do not invent a method because a similarly named dashboard report exists.

Review connector-catalog.csv by needed capability, not as an instruction to provision all 28 interfaces. The catalog is scope inventory, not a statement that adapters are implemented. Mark partial/unsupported capability explicitly and continue independent work.

## Sources and runtime

- Wix: read wix.md, verify apps/target/scopes and owner per field.
- GSC: qualify property/OAuth readonly, Search Analytics/inspection/sitemap methods; distinguish UI-only reports and actual available API.
- Bing: use current REST JSON, not retired SOAP/POX examples; qualify AI report export/API separately.
- IndexNow: verify host/key and changed public URL scope; received is not indexed. Deduplicate changes, respect current limits/429.
- Crawler/Firecrawl: bounded public targets; original HTML/headers where available; actual target status versus API success; budget/retention.
- Browser: only direct authorized interaction or permitted plugin fallback; never infer a live test from in-memory SSR.
- CI/code: exact checkout/revision and generated artifacts; inspect existing tools before building another auditor.
- CDN/logs: identify actual provider/account/host; a Cloudflare plugin does not prove the site uses that account.
- Analytics/CMP: first qualify purpose/surfaces/fields and existing scripts; read aggregate minimal data only.
- Scheduler/coordinator: inspect existing routines/events; choose a single supported runner and authority. Do not create a recurring job just because this skill supports one.
- Models: provider/version/data terms/cost and actual interface must be known; API output need not reproduce a web-search product.

## Orchestrate by need

Use one lead SEO/GEO role to maintain task/intent/evidence. Invoke technical, editorial, locale, UX/media, measurement and security reviewers when useful; these roles do not require permanent processes. Reuse the existing candidate SEO core and project coordinator when qualified.

Use deterministic extraction/checks for objective rules and models for diagnosis/synthesis. A review packet contains bounded scope, source revision/hash, necessary public content/code, concrete question and output contract. Keep independent reviewers from earlier conclusions before first delivery. Consolidate by cause/evidence, not majority vote. Never name an internal role Claude/Gemini/Copilot without actually using that provider.

Competent humans retain actual clinical/commercial/translation review responsibilities. No synthetic signatures, receipts, leases or coordinator replies.

## Events, concurrency and failures

Validate event source/signature where provided; record event ID and target. Handle duplicates, delay and reordering. Debounce public changes and reconcile missed/unsupported events. No webhook support is presumed.

Use the existing lock/lease mechanism keyed to site/resource/locale/field. Re-read current baseline immediately before replace-style APIs. A lock local to the agent does not guarantee exclusion of dashboard writers.

| Outcome | Response |
|---|---|
| 401/expired token | Use supported authorized renewal; otherwise mark unavailable without leaking secrets |
| 403/permission denied | Identify missing operation permission; do not probe other sites or add privilege |
| 429/Retry-After | Respect backoff and quota; postpone lower-priority work |
| Read timeout | Mark unknown; bounded appropriate retry, not proof the page is down |
| Write timeout/partial | Reconcile receipt/current state before any retry; no duplicate effect |
| Version/owner drift | Reconcile limited delta; do not overwrite intervening work |
| Missing connector | Preserve evidence and manual/candidate path; no fictional completion |

Separate public-data crawling from write credentials. Use allowlisted public destinations, no SSRF/private networks and no patient endpoints. Minimize outputs before external models. Keep credentials out of skill/package/logs.
